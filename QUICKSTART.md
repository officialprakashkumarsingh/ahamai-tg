# 🚀 Quick Start Guide

Get your AhamAI Telegram Bot running in minutes!

## 🏃‍♂️ Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Test Configuration
```bash
python test_bot.py
```

### 4. Run the Bot
```bash
python bot.py
```

## 🌐 Deploy to Render

### Option 1: One-Click Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Option 2: Manual Deploy
1. **Fork this repository** to your GitHub account
2. **Connect to Render** and create a new Web Service
3. **Set environment variables**:
   - `TELEGRAM_BOT_TOKEN`: Your bot token from @BotFather
   - `API_BASE_URL`: https://ahamai-api.officialprakashkrsingh.workers.dev
   - `API_KEY`: ahamaibyprakash25
   - `BOT_USERNAME`: ahamai_tgbot
4. **Deploy** and wait for completion

## 🤖 Test Your Bot

1. Open Telegram and search for `@ahamai_tgbot`
2. Send `/start` to begin
3. Try these commands:
   - `/help` - Get help
   - `/models` - See available AI models
   - `/settings` - Configure preferences
   - Just chat normally!

## 🔧 Environment Variables

Create a `.env` file with:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
API_BASE_URL=https://ahamai-api.officialprakashkrsingh.workers.dev
API_KEY=ahamaibyprakash25
BOT_USERNAME=ahamai_tgbot
```

## 📱 Bot Features

- 🧠 **20+ AI Models** (GPT, Claude, Gemini, DeepSeek)
- 💬 **Smart Conversations** with context memory
- 👥 **Group & Private** chat support
- 🔧 **Admin Commands** for group management
- ⚙️ **User Settings** and preferences
- 📊 **Statistics** and monitoring

## 🆘 Need Help?

- 📖 **Full Documentation**: See [README.md](README.md)
- 🚀 **Deployment Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- 🐛 **Issues**: Create a GitHub issue
- 💬 **Test Bot**: Message @ahamai_tgbot on Telegram

Happy chatting! 🎉