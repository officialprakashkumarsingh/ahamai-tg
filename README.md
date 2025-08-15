# 🤖 AhamAI Telegram Bot

A powerful and intelligent Telegram bot powered by multiple AI models through an OpenAI-compatible API. AhamAI provides smart conversation capabilities, group management features, and seamless integration with various AI models.

## ✨ Features

### 🧠 AI-Powered Conversations
- **Multi-Model Support**: Access to 20+ AI models including GPT-4o, Claude, Gemini, DeepSeek, and more
- **Context-Aware**: Remembers conversation history for natural, flowing discussions
- **Smart Response Logic**: Responds appropriately in groups (when mentioned or replied to)
- **Model Selection**: Users can choose their preferred AI model

### 👥 Group & Private Chat Support
- **Private Chats**: Direct one-on-one conversations
- **Group Integration**: Smart group participation with context awareness
- **User Recognition**: Tracks usernames and provides personalized responses
- **Mention Detection**: Responds when mentioned with @ahamai_tgbot

### 🔧 Advanced Group Management (Admin Only)
- **Moderation**: Kick, ban, unban, mute, unmute users
- **Message Management**: Pin and unpin messages
- **Warning System**: Track user warnings with automatic escalation
- **Permission Checks**: Ensures proper admin privileges before actions

### ⚙️ Smart Features
- **Interactive Settings**: Easy model switching with inline keyboards
- **Statistics Tracking**: User and bot usage statistics
- **Error Handling**: Robust error handling with user-friendly messages
- **Conversation Management**: Clear conversation history when needed

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Telegram Bot Token
- API access to AhamAI service

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ahamai-telegram-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

### 🌐 Deploy on Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. **Connect your GitHub repository** to Render
2. **Use the provided `render.yaml`** for automatic configuration
3. **Set environment variables** in Render dashboard:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `API_BASE_URL`: https://ahamai-api.officialprakashkrsingh.workers.dev
   - `API_KEY`: Your AhamAI API key
   - `BOT_USERNAME`: ahamai_tgbot

4. **Deploy** and your bot will be live!

## 📱 Bot Commands

### Basic Commands
- `/start` - Welcome message and bot introduction
- `/help` - Show all available commands and features
- `/models` - List all available AI models
- `/settings` - Configure your preferences and select models
- `/clear` - Clear conversation history
- `/stats` - Show bot and usage statistics

### Group Commands
- `/groupinfo` - Display group information and bot status

### Admin Commands (Groups Only)
- `/kick` - Kick a user from the group
- `/ban` - Ban a user from the group
- `/unban <user_id>` - Unban a user
- `/mute` - Mute a user (reply to their message)
- `/unmute` - Unmute a user (reply to their message)
- `/pin` - Pin a message (reply to the message)
- `/unpin` - Unpin a message or all pinned messages
- `/warn` - Warn a user (reply to their message)
- `/warnings` - Check warning count for a user

## 🔧 Configuration

### Environment Variables
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
API_BASE_URL=https://ahamai-api.officialprakashkrsingh.workers.dev
API_KEY=your_api_key
BOT_USERNAME=ahamai_tgbot
```

### Available AI Models
The bot supports 20+ AI models including:
- **GPT Models**: gpt-4o, gpt-4o-mini, gpt-5, gpt-5-mini
- **Claude Models**: claude-sonnet-4, claude-opus-4
- **Gemini Models**: gemini-2.0-flash, gemini-2.5-flash
- **DeepSeek Models**: deepseek-r1, deepseek-r1-distill
- **Other Models**: perplexed, felo, exaanswer, and more

## 💬 Usage Examples

### Private Chat
```
User: Hello AhamAI!
Bot: Hello! I'm AhamAI, your intelligent AI assistant. How can I help you today?

User: What's the weather like?
Bot: I'd be happy to help with weather information! However, I don't have access to real-time weather data. Could you let me know your location so I can provide general guidance on where to find current weather information?
```

### Group Chat
```
User: @ahamai_tgbot what's 2+2?
Bot: 2 + 2 = 4! 😊

User: (replies to bot's message) Can you explain why?
Bot: Of course! Addition is one of the basic arithmetic operations...
```

### Model Selection
```
User: /settings
Bot: (Shows interactive keyboard with model options)
User: (Clicks on "gpt-4o")
Bot: ✅ Model Updated! Your preferred model is now: gpt-4o
```

## 🏗️ Architecture

### Core Components
- **`bot.py`**: Main bot application with conversation handling
- **`admin_commands.py`**: Group management and moderation features
- **`requirements.txt`**: Python dependencies
- **`.env`**: Environment configuration

### Key Features
- **Async/Await**: Full asynchronous operation for better performance
- **Context Management**: Maintains conversation context per user/group
- **Error Handling**: Comprehensive error handling with logging
- **Modular Design**: Separated admin commands for maintainability

## 🔒 Security & Privacy

- **Token Security**: Bot token and API keys stored securely in environment variables
- **Permission Checks**: Admin commands verify user permissions before execution
- **Rate Limiting**: Built-in protection against spam and abuse
- **Data Privacy**: Conversation data stored temporarily in memory only

## 🐛 Troubleshooting

### Common Issues

1. **Bot doesn't respond in groups**
   - Make sure to mention the bot with @ahamai_tgbot
   - Or reply to the bot's messages
   - Check if the bot has necessary permissions

2. **Admin commands not working**
   - Verify you have admin privileges in the group
   - Ensure the bot has admin permissions
   - Check if you're using the commands correctly

3. **API errors**
   - Verify your API key is correct
   - Check if the API service is available
   - Look at the logs for detailed error messages

### Debug Mode
Enable debug logging by modifying the logging level in `bot.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Monitoring

The bot provides built-in statistics tracking:
- Active conversations count
- Total messages processed
- Available models count
- User-specific statistics

Access with `/stats` command or through the settings menu.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **GitHub Issues**: Report bugs or request features
- **Telegram**: Contact @ahamai_tgbot for bot-related queries
- **Documentation**: Check this README for comprehensive information

## 🙏 Acknowledgments

- **python-telegram-bot**: Excellent Telegram Bot API wrapper
- **AhamAI API**: Powerful multi-model AI service
- **Render**: Easy deployment platform
- **OpenAI**: API compatibility standard

---

**Bot URL**: [@ahamai_tgbot](http://t.me/ahamai_tgbot)

**Made with ❤️ and 🤖 AI**