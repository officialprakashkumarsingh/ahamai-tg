import os
import json
import logging
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional, Any
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    CallbackQueryHandler, ContextTypes, filters
)
from telegram.constants import ParseMode, ChatMemberStatus
from dotenv import load_dotenv
from admin_commands import AdminCommands

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class AhamAI:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.api_base_url = os.getenv('API_BASE_URL')
        self.api_key = os.getenv('API_KEY')
        self.username = os.getenv('BOT_USERNAME')
        
        # Bot configuration
        self.max_tokens = 2000
        self.temperature = 0.7
        self.default_model = "gpt-4o-mini"
        
        # Storage for conversation context
        self.conversations: Dict[str, List[Dict]] = {}
        self.user_preferences: Dict[str, Dict] = {}
        self.group_settings: Dict[str, Dict] = {}
        
        # Available models
        self.models: List[str] = []
        
        # Initialize admin commands
        self.admin_commands = AdminCommands(self)
        
    async def fetch_models(self) -> List[str]:
        """Fetch available models from the API"""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/v1/models", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.models = [model["id"] for model in data.get("data", [])]
                        logger.info(f"Fetched {len(self.models)} models")
                        return self.models
                    else:
                        logger.error(f"Failed to fetch models: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error fetching models: {e}")
            return []

    async def chat_completion(self, messages: List[Dict], model: str = None, user_id: str = None) -> str:
        """Make API call to get chat completion"""
        try:
            if not model:
                model = self.user_preferences.get(user_id, {}).get('model', self.default_model)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "stream": False
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.api_base_url}/v1/chat/completions", 
                                      headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['choices'][0]['message']['content']
                    else:
                        error_text = await response.text()
                        logger.error(f"API Error {response.status}: {error_text}")
                        return "Sorry, I encountered an error processing your request. Please try again."
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            return "Sorry, I'm having trouble connecting to my AI service. Please try again later."

    def get_conversation_key(self, update: Update) -> str:
        """Generate unique conversation key for user/group"""
        if update.effective_chat.type == 'private':
            return f"user_{update.effective_user.id}"
        else:
            return f"group_{update.effective_chat.id}"

    def add_to_conversation(self, key: str, role: str, content: str, username: str = None):
        """Add message to conversation history"""
        if key not in self.conversations:
            self.conversations[key] = []
        
        message = {"role": role, "content": content}
        if username and role == "user":
            message["content"] = f"[{username}]: {content}"
        
        self.conversations[key].append(message)
        
        # Keep only last 20 messages to prevent token overflow
        if len(self.conversations[key]) > 20:
            self.conversations[key] = self.conversations[key][-20:]

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        chat = update.effective_chat
        
        welcome_message = f"""
🤖 **Welcome to AhamAI!** 

Hello {user.first_name}! I'm AhamAI, your intelligent AI assistant.

🔹 **What I can do:**
• Answer questions and have conversations
• Work in groups and private chats
• Remember conversation context
• Use multiple AI models
• Help with various tasks

🔹 **Commands:**
/help - Show all commands
/models - View available AI models
/settings - Configure preferences
/clear - Clear conversation history
/stats - Show bot statistics

{"🔹 **Group Features:**" if chat.type != 'private' else ""}
{"• Mention me with @" + self.username + " or reply to my messages" if chat.type != 'private' else ""}
{"• I can see all messages for better context" if chat.type != 'private' else ""}
{"• Group management commands (for admins)" if chat.type != 'private' else ""}

Let's start chatting! 🚀
        """
        
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **AhamAI Commands & Features**

**Basic Commands:**
/start - Welcome message and introduction
/help - Show this help message
/models - List available AI models
/settings - Configure your preferences
/clear - Clear conversation history
/stats - Show usage statistics

**Chat Features:**
• Just send me any message to start chatting
• I remember our conversation context
• I can handle complex questions and tasks

**Group Features:**
• Mention me with @ahamai_tgbot to get my attention
• Reply to my messages to continue conversations
• I can see all group messages for better context

**Model Selection:**
• Use /models to see available AI models
• Change model in /settings
• Different models have different capabilities

**Smart Features:**
• Context-aware responses
• Multi-turn conversations
• Code assistance
• Creative writing
• Problem solving

**Group Admin Commands:**
/groupinfo - Show group information
/botpermissions - Check bot permissions

Need help with something specific? Just ask! 😊
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

    async def models_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /models command"""
        if not self.models:
            await self.fetch_models()
        
        if not self.models:
            await update.message.reply_text("❌ Unable to fetch available models. Please try again later.")
            return
        
        models_text = "🤖 **Available AI Models:**\n\n"
        
        # Group models by type
        gpt_models = [m for m in self.models if 'gpt' in m.lower()]
        claude_models = [m for m in self.models if 'claude' in m.lower()]
        gemini_models = [m for m in self.models if 'gemini' in m.lower()]
        deepseek_models = [m for m in self.models if 'deepseek' in m.lower()]
        other_models = [m for m in self.models if not any(x in m.lower() for x in ['gpt', 'claude', 'gemini', 'deepseek'])]
        
        if gpt_models:
            models_text += "**🧠 GPT Models:**\n"
            for model in gpt_models[:5]:  # Show first 5
                models_text += f"• `{model}`\n"
            models_text += "\n"
        
        if claude_models:
            models_text += "**🎭 Claude Models:**\n"
            for model in claude_models[:3]:
                models_text += f"• `{model}`\n"
            models_text += "\n"
        
        if gemini_models:
            models_text += "**💎 Gemini Models:**\n"
            for model in gemini_models[:3]:
                models_text += f"• `{model}`\n"
            models_text += "\n"
        
        if other_models:
            models_text += "**🔬 Other Models:**\n"
            for model in other_models[:5]:
                models_text += f"• `{model}`\n"
        
        models_text += f"\n📊 **Total Models Available:** {len(self.models)}\n"
        models_text += "💡 Use /settings to change your preferred model"
        
        await update.message.reply_text(models_text, parse_mode=ParseMode.MARKDOWN)

    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /settings command"""
        user_id = str(update.effective_user.id)
        current_model = self.user_preferences.get(user_id, {}).get('model', self.default_model)
        
        keyboard = []
        popular_models = ['gpt-4o', 'gpt-4o-mini', 'claude-sonnet-4-20250514', 'gemini-2.0-flash', 'deepseek-r1']
        
        for model in popular_models:
            if model in self.models:
                button_text = f"{'✅ ' if model == current_model else ''}{model}"
                keyboard.append([InlineKeyboardButton(button_text, callback_data=f"model_{model}")])
        
        keyboard.append([InlineKeyboardButton("🔄 Show All Models", callback_data="show_all_models")])
        keyboard.append([InlineKeyboardButton("📊 My Stats", callback_data="user_stats")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        settings_text = f"""
⚙️ **Settings for {update.effective_user.first_name}**

**Current Model:** `{current_model}`
**Total Messages:** {len(self.conversations.get(f"user_{user_id}", []))}

Choose a model below or customize other settings:
        """
        
        await update.message.reply_text(settings_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(update.effective_user.id)
        
        if query.data.startswith("model_"):
            model = query.data.replace("model_", "")
            if user_id not in self.user_preferences:
                self.user_preferences[user_id] = {}
            self.user_preferences[user_id]['model'] = model
            
            await query.edit_message_text(
                f"✅ **Model Updated!**\n\nYour preferred model is now: `{model}`\n\n💡 This will be used for all your future conversations.",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif query.data == "show_all_models":
            if not self.models:
                await self.fetch_models()
            
            models_text = "🤖 **All Available Models:**\n\n"
            for i, model in enumerate(self.models, 1):
                models_text += f"{i}. `{model}`\n"
                if i % 10 == 0:  # Break every 10 models
                    models_text += "\n"
            
            await query.edit_message_text(models_text, parse_mode=ParseMode.MARKDOWN)
        
        elif query.data == "user_stats":
            conv_key = f"user_{user_id}"
            message_count = len(self.conversations.get(conv_key, []))
            current_model = self.user_preferences.get(user_id, {}).get('model', self.default_model)
            
            stats_text = f"""
📊 **Your Statistics**

**Messages in conversation:** {message_count}
**Current model:** `{current_model}`
**User ID:** `{user_id}`
**Joined:** Today (session-based)

💡 Use /clear to reset conversation history
            """
            
            await query.edit_message_text(stats_text, parse_mode=ParseMode.MARKDOWN)

    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /clear command"""
        conv_key = self.get_conversation_key(update)
        if conv_key in self.conversations:
            del self.conversations[conv_key]
        
        await update.message.reply_text(
            "🧹 **Conversation cleared!**\n\nYour conversation history has been reset. We can start fresh now! 🆕"
        )

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        total_conversations = len(self.conversations)
        total_messages = sum(len(conv) for conv in self.conversations.values())
        
        stats_text = f"""
📊 **AhamAI Statistics**

**Active Conversations:** {total_conversations}
**Total Messages Processed:** {total_messages}
**Available Models:** {len(self.models)}
**Uptime:** Session-based

**Popular Features:**
• Multi-model AI chat
• Group conversation support
• Context-aware responses
• Smart conversation management

🤖 Powered by multiple AI models for the best experience!
        """
        
        await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)

    async def group_info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /groupinfo command (groups only)"""
        if update.effective_chat.type == 'private':
            await update.message.reply_text("❌ This command is only available in groups.")
            return
        
        chat = update.effective_chat
        user = update.effective_user
        
        # Get user's status in the group
        try:
            member = await context.bot.get_chat_member(chat.id, user.id)
            user_status = member.status
        except:
            user_status = "unknown"
        
        # Get bot's permissions
        try:
            bot_member = await context.bot.get_chat_member(chat.id, context.bot.id)
            bot_status = bot_member.status
            bot_permissions = bot_member.can_delete_messages, bot_member.can_restrict_members
        except:
            bot_status = "unknown"
            bot_permissions = (False, False)
        
        conv_key = f"group_{chat.id}"
        message_count = len(self.conversations.get(conv_key, []))
        
        info_text = f"""
👥 **Group Information**

**Group:** {chat.title}
**Group ID:** `{chat.id}`
**Your Status:** {user_status}
**Bot Status:** {bot_status}

**Conversation Stats:**
**Messages:** {message_count}
**Active:** {'Yes' if conv_key in self.conversations else 'No'}

**Bot Capabilities:**
• See all messages: ✅
• Context awareness: ✅
• Multi-user support: ✅
• Admin commands: {'✅' if user_status in ['administrator', 'creator'] else '❌'}

💡 Mention @{self.username} or reply to my messages to interact!
        """
        
        await update.message.reply_text(info_text, parse_mode=ParseMode.MARKDOWN)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        user = update.effective_user
        chat = update.effective_chat
        message = update.message
        
        # Check if bot should respond in groups
        should_respond = False
        if chat.type == 'private':
            should_respond = True
        elif message.reply_to_message and message.reply_to_message.from_user.id == context.bot.id:
            should_respond = True
        elif f"@{self.username}" in message.text:
            should_respond = True
        elif message.text.lower().startswith(('aham', 'ai', 'bot')):
            should_respond = True
        
        if not should_respond and chat.type != 'private':
            # Store message for context but don't respond
            conv_key = self.get_conversation_key(update)
            self.add_to_conversation(conv_key, "user", message.text, user.username or user.first_name)
            return
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=chat.id, action="typing")
        
        # Prepare conversation
        conv_key = self.get_conversation_key(update)
        
        # Clean message text
        clean_text = message.text
        if f"@{self.username}" in clean_text:
            clean_text = clean_text.replace(f"@{self.username}", "").strip()
        
        # Add system message for context if needed
        if conv_key not in self.conversations:
            system_message = "You are AhamAI, a helpful and intelligent AI assistant. "
            if chat.type != 'private':
                system_message += f"You're in a group chat '{chat.title}' with multiple users. "
                system_message += "You can see all messages for context but only respond when mentioned or replied to. "
                system_message += "Be conversational and engaging while being helpful."
            else:
                system_message += "You're in a private chat. Be helpful, friendly, and engaging."
            
            self.conversations[conv_key] = [{"role": "system", "content": system_message}]
        
        # Add user message
        username = user.username or user.first_name
        self.add_to_conversation(conv_key, "user", clean_text, username if chat.type != 'private' else None)
        
        # Get AI response
        user_id = str(user.id)
        response = await self.chat_completion(self.conversations[conv_key], user_id=user_id)
        
        # Add AI response to conversation
        self.add_to_conversation(conv_key, "assistant", response)
        
        # Send response
        try:
            await message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        except:
            # Fallback without markdown if parsing fails
            await message.reply_text(response)

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    # Initialize bot
    aham_ai = AhamAI()
    
    # Create application
    application = Application.builder().token(aham_ai.token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", aham_ai.start_command))
    application.add_handler(CommandHandler("help", aham_ai.help_command))
    application.add_handler(CommandHandler("models", aham_ai.models_command))
    application.add_handler(CommandHandler("settings", aham_ai.settings_command))
    application.add_handler(CommandHandler("clear", aham_ai.clear_command))
    application.add_handler(CommandHandler("stats", aham_ai.stats_command))
    application.add_handler(CommandHandler("groupinfo", aham_ai.group_info_command))
    
    # Admin command handlers
    application.add_handler(CommandHandler("kick", aham_ai.admin_commands.kick_command))
    application.add_handler(CommandHandler("ban", aham_ai.admin_commands.ban_command))
    application.add_handler(CommandHandler("unban", aham_ai.admin_commands.unban_command))
    application.add_handler(CommandHandler("mute", aham_ai.admin_commands.mute_command))
    application.add_handler(CommandHandler("unmute", aham_ai.admin_commands.unmute_command))
    application.add_handler(CommandHandler("pin", aham_ai.admin_commands.pin_command))
    application.add_handler(CommandHandler("unpin", aham_ai.admin_commands.unpin_command))
    application.add_handler(CommandHandler("warn", aham_ai.admin_commands.warn_command))
    application.add_handler(CommandHandler("warnings", aham_ai.admin_commands.warnings_command))
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(aham_ai.button_callback))
    
    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, aham_ai.handle_message))
    
    # Error handler
    application.add_error_handler(aham_ai.error_handler)
    
    # Fetch models on startup
    async def post_init(application):
        await aham_ai.fetch_models()
        logger.info(f"AhamAI bot started with {len(aham_ai.models)} models available")
    
    application.post_init = post_init
    
    # Start the bot
    logger.info("Starting AhamAI Telegram Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()