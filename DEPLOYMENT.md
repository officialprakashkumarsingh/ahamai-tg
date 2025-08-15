# 🚀 Deployment Guide for AhamAI Telegram Bot

This guide will help you deploy the AhamAI Telegram Bot on Render, a modern cloud platform.

## 📋 Prerequisites

Before deployment, ensure you have:

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Telegram Bot Token** - From @BotFather on Telegram
4. **AhamAI API Key** - Access to the AhamAI API service

## 🔧 Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Fork or Clone** this repository to your GitHub account
2. **Verify files** are present:
   - `bot.py` (main bot file)
   - `admin_commands.py` (admin features)
   - `requirements.txt` (dependencies)
   - `render.yaml` (deployment config)
   - `.env.example` (environment template)

### Step 2: Create Render Service

1. **Login to Render** at [dashboard.render.com](https://dashboard.render.com)
2. **Click "New"** and select **"Web Service"**
3. **Connect GitHub** repository containing your bot code
4. **Configure the service:**
   - **Name**: `ahamai-telegram-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`

### Step 3: Configure Environment Variables

In the Render dashboard, add these environment variables:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `TELEGRAM_BOT_TOKEN` | `8296595788:AAH9sWfwG6O886QPxd5mVCGb_RTEwsYj9nA` | Your Telegram bot token |
| `API_BASE_URL` | `https://ahamai-api.officialprakashkrsingh.workers.dev` | AhamAI API endpoint |
| `API_KEY` | `ahamaibyprakash25` | Your AhamAI API key |
| `BOT_USERNAME` | `ahamai_tgbot` | Your bot's username |

### Step 4: Deploy

1. **Click "Create Web Service"**
2. **Wait for deployment** (usually 2-5 minutes)
3. **Check logs** for any errors
4. **Verify deployment** - look for "AhamAI bot started" message

### Step 5: Test Your Bot

1. **Open Telegram** and search for `@ahamai_tgbot`
2. **Send `/start`** command
3. **Test basic functionality**:
   - Send a regular message
   - Try `/models` command
   - Test `/settings` command

## 🔍 Monitoring & Troubleshooting

### Checking Deployment Status

**Render Dashboard:**
- Service status (Running/Failed)
- Real-time logs
- CPU and memory usage
- Deployment history

**Common Log Messages:**
```
✅ SUCCESS: "AhamAI bot started with X models available"
❌ ERROR: "Failed to fetch models" - Check API key/URL
❌ ERROR: "Update failed" - Check bot token
```

### Common Issues & Solutions

#### 1. Bot Not Responding
**Symptoms:** Bot doesn't reply to messages
**Solutions:**
- Check if service is "Running" in Render dashboard
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Check logs for errors

#### 2. API Errors
**Symptoms:** "Sorry, I encountered an error" responses
**Solutions:**
- Verify `API_KEY` is correct
- Check `API_BASE_URL` is accessible
- Monitor API service status

#### 3. Deployment Fails
**Symptoms:** Service stuck in "Deploy Failed" state
**Solutions:**
- Check `requirements.txt` syntax
- Verify Python version compatibility
- Review build logs for specific errors

#### 4. Memory/Performance Issues
**Symptoms:** Bot responds slowly or crashes
**Solutions:**
- Monitor memory usage in dashboard
- Consider upgrading to paid plan for more resources
- Check for memory leaks in logs

### Log Monitoring

**Key Log Patterns to Watch:**
```bash
# Successful startup
INFO - AhamAI bot started with 22 models available

# API calls
INFO - Fetched 22 models
ERROR - API Error 401: Unauthorized

# User interactions
INFO - Update 123456789 from user @username
ERROR - Update 123456789 caused error: ...
```

### Performance Optimization

**Render Free Tier Limitations:**
- Service sleeps after 15 minutes of inactivity
- 750 hours/month limit
- Shared CPU resources

**Optimization Tips:**
- Consider upgrading to paid plan for 24/7 availability
- Monitor resource usage regularly
- Use efficient conversation context management

## 🔄 Updates & Maintenance

### Updating Your Bot

1. **Push changes** to your GitHub repository
2. **Render will auto-deploy** (if auto-deploy is enabled)
3. **Monitor deployment** in dashboard
4. **Test functionality** after deployment

### Manual Deployment

If auto-deploy is disabled:
1. **Go to Render dashboard**
2. **Click "Manual Deploy"**
3. **Select "Deploy latest commit"**
4. **Monitor deployment progress**

### Backup & Recovery

**Configuration Backup:**
- Save environment variables securely
- Keep a copy of your repository
- Document any custom configurations

**Recovery Process:**
1. **Check service status** in dashboard
2. **Review recent logs** for error patterns
3. **Redeploy** if necessary
4. **Verify environment variables**

## 💰 Cost Considerations

### Free Tier
- **Perfect for testing** and small-scale use
- **750 hours/month** included
- **Service sleeps** after 15 minutes idle

### Paid Plans
- **Starting at $7/month** for always-on service
- **Better performance** and reliability
- **Custom domains** and SSL certificates

## 🔐 Security Best Practices

### Environment Variables
- **Never commit** tokens/keys to repository
- **Use Render's environment** variable system
- **Rotate keys** regularly

### Access Control
- **Limit repository access** to authorized users
- **Use GitHub's security features**
- **Monitor deployment logs** for suspicious activity

### API Security
- **Monitor API usage** for unusual patterns
- **Set up rate limiting** if possible
- **Keep API keys confidential**

## 📞 Support & Resources

### Render Support
- **Documentation**: [render.com/docs](https://render.com/docs)
- **Community**: [community.render.com](https://community.render.com)
- **Status Page**: [status.render.com](https://status.render.com)

### Bot Support
- **GitHub Issues**: Report bugs in repository
- **Telegram**: Test with @ahamai_tgbot
- **Documentation**: This README and deployment guide

### Useful Resources
- **Telegram Bot API**: [core.telegram.org/bots/api](https://core.telegram.org/bots/api)
- **python-telegram-bot**: [docs.python-telegram-bot.org](https://docs.python-telegram-bot.org)
- **Render Python Guide**: [render.com/docs/deploy-python](https://render.com/docs/deploy-python)

---

## 🎉 Congratulations!

Your AhamAI Telegram Bot should now be successfully deployed and running on Render! 

**Next Steps:**
1. Share your bot with friends and groups
2. Monitor usage and performance
3. Consider upgrading for 24/7 availability
4. Explore additional features and customizations

**Bot URL**: [@ahamai_tgbot](http://t.me/ahamai_tgbot)