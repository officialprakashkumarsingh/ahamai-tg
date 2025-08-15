"""
Admin commands module for AhamAI Telegram Bot
Provides advanced group management features
"""

from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus, ParseMode
import logging

logger = logging.getLogger(__name__)

class AdminCommands:
    def __init__(self, bot_instance):
        self.bot = bot_instance
    
    async def is_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int = None) -> bool:
        """Check if user is admin in the group"""
        if update.effective_chat.type == 'private':
            return True
        
        try:
            user_id = user_id or update.effective_user.id
            member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
            return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
        except:
            return False
    
    async def kick_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Kick a user from the group (admin only)"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ You need to be an admin to use this command.")
            return
        
        if not context.args:
            await update.message.reply_text("❌ Please specify a user ID or reply to a message.")
            return
        
        try:
            if update.message.reply_to_message:
                user_id = update.message.reply_to_message.from_user.id
                username = update.message.reply_to_message.from_user.username or "User"
            else:
                user_id = int(context.args[0])
                username = f"User {user_id}"
            
            # Check if bot has permission
            bot_member = await context.bot.get_chat_member(update.effective_chat.id, context.bot.id)
            if not bot_member.can_restrict_members:
                await update.message.reply_text("❌ I don't have permission to kick members.")
                return
            
            await context.bot.ban_chat_member(update.effective_chat.id, user_id)
            await context.bot.unban_chat_member(update.effective_chat.id, user_id)
            
            await update.message.reply_text(f"✅ {username} has been kicked from the group.")
            
        except ValueError:
            await update.message.reply_text("❌ Invalid user ID.")
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to kick user: {str(e)}")
    
    async def ban_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ban a user from the group (admin only)"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ You need to be an admin to use this command.")
            return
        
        if not context.args and not update.message.reply_to_message:
            await update.message.reply_text("❌ Please specify a user ID or reply to a message.")
            return
        
        try:
            if update.message.reply_to_message:
                user_id = update.message.reply_to_message.from_user.id
                username = update.message.reply_to_message.from_user.username or "User"
            else:
                user_id = int(context.args[0])
                username = f"User {user_id}"
            
            # Check if bot has permission
            bot_member = await context.bot.get_chat_member(update.effective_chat.id, context.bot.id)
            if not bot_member.can_restrict_members:
                await update.message.reply_text("❌ I don't have permission to ban members.")
                return
            
            await context.bot.ban_chat_member(update.effective_chat.id, user_id)
            await update.message.reply_text(f"🚫 {username} has been banned from the group.")
            
        except ValueError:
            await update.message.reply_text("❌ Invalid user ID.")
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to ban user: {str(e)}")
    
    async def unban_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Unban a user from the group (admin only)"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ You need to be an admin to use this command.")
            return
        
        if not context.args:
            await update.message.reply_text("❌ Please specify a user ID.")
            return
        
        try:
            user_id = int(context.args[0])
            
            # Check if bot has permission
            bot_member = await context.bot.get_chat_member(update.effective_chat.id, context.bot.id)
            if not bot_member.can_restrict_members:
                await update.message.reply_text("❌ I don't have permission to unban members.")
                return
            
            await context.bot.unban_chat_member(update.effective_chat.id, user_id)
            await update.message.reply_text(f"✅ User {user_id} has been unbanned.")
            
        except ValueError:
            await update.message.reply_text("❌ Invalid user ID.")
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to unban user: {str(e)}")
    
    async def mute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mute a user in the group (admin only)"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ You need to be an admin to use this command.")
            return
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to a message to mute the user.")
            return
        
        try:
            user_id = update.message.reply_to_message.from_user.id
            username = update.message.reply_to_message.from_user.username or "User"
            
            # Check if bot has permission
            bot_member = await context.bot.get_chat_member(update.effective_chat.id, context.bot.id)
            if not bot_member.can_restrict_members:
                await update.message.reply_text("❌ I don't have permission to restrict members.")
                return
            
            from telegram import ChatPermissions
            await context.bot.restrict_chat_member(
                update.effective_chat.id, 
                user_id,
                permissions=ChatPermissions(can_send_messages=False)
            )
            
            await update.message.reply_text(f"🔇 {username} has been muted.")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to mute user: {str(e)}")
    
    async def unmute_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Unmute a user in the group (admin only)"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ You need to be an admin to use this command.")
            return
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to a message to unmute the user.")
            return
        
        try:
            user_id = update.message.reply_to_message.from_user.id
            username = update.message.reply_to_message.from_user.username or "User"
            
            # Check if bot has permission
            bot_member = await context.bot.get_chat_member(update.effective_chat.id, context.bot.id)
            if not bot_member.can_restrict_members:
                await update.message.reply_text("❌ I don't have permission to restrict members.")
                return
            
            from telegram import ChatPermissions
            await context.bot.restrict_chat_member(
                update.effective_chat.id, 
                user_id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )
            
            await update.message.reply_text(f"🔊 {username} has been unmuted.")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to unmute user: {str(e)}")
    
    async def pin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Pin a message (admin only)"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ You need to be an admin to use this command.")
            return
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to a message to pin it.")
            return
        
        try:
            # Check if bot has permission
            bot_member = await context.bot.get_chat_member(update.effective_chat.id, context.bot.id)
            if not bot_member.can_pin_messages:
                await update.message.reply_text("❌ I don't have permission to pin messages.")
                return
            
            await context.bot.pin_chat_message(
                update.effective_chat.id,
                update.message.reply_to_message.message_id
            )
            
            await update.message.reply_text("📌 Message pinned successfully!")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to pin message: {str(e)}")
    
    async def unpin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Unpin a message (admin only)"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ You need to be an admin to use this command.")
            return
        
        try:
            # Check if bot has permission
            bot_member = await context.bot.get_chat_member(update.effective_chat.id, context.bot.id)
            if not bot_member.can_pin_messages:
                await update.message.reply_text("❌ I don't have permission to unpin messages.")
                return
            
            if update.message.reply_to_message:
                await context.bot.unpin_chat_message(
                    update.effective_chat.id,
                    update.message.reply_to_message.message_id
                )
            else:
                await context.bot.unpin_all_chat_messages(update.effective_chat.id)
            
            await update.message.reply_text("📌 Message(s) unpinned successfully!")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to unpin message: {str(e)}")
    
    async def warn_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Warn a user (admin only)"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ You need to be an admin to use this command.")
            return
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to a message to warn the user.")
            return
        
        try:
            user_id = update.message.reply_to_message.from_user.id
            username = update.message.reply_to_message.from_user.username or "User"
            reason = " ".join(context.args) if context.args else "No reason provided"
            
            # Store warning (in real implementation, you'd use a database)
            group_id = str(update.effective_chat.id)
            if group_id not in self.bot.group_settings:
                self.bot.group_settings[group_id] = {}
            if 'warnings' not in self.bot.group_settings[group_id]:
                self.bot.group_settings[group_id]['warnings'] = {}
            
            user_warnings = self.bot.group_settings[group_id]['warnings'].get(str(user_id), 0) + 1
            self.bot.group_settings[group_id]['warnings'][str(user_id)] = user_warnings
            
            warn_text = f"⚠️ **Warning #{user_warnings}** for {username}\n\n**Reason:** {reason}"
            
            if user_warnings >= 3:
                warn_text += f"\n\n🚫 User has reached 3 warnings and should be considered for action."
            
            await update.message.reply_text(warn_text, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to warn user: {str(e)}")
    
    async def warnings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check warnings for a user"""
        try:
            if update.message.reply_to_message:
                user_id = update.message.reply_to_message.from_user.id
                username = update.message.reply_to_message.from_user.username or "User"
            else:
                user_id = update.effective_user.id
                username = update.effective_user.username or "You"
            
            group_id = str(update.effective_chat.id)
            warnings = self.bot.group_settings.get(group_id, {}).get('warnings', {}).get(str(user_id), 0)
            
            await update.message.reply_text(f"⚠️ {username} has **{warnings}** warning(s).", parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to check warnings: {str(e)}")