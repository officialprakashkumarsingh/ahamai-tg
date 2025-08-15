#!/usr/bin/env python3
"""
Test script for AhamAI Telegram Bot
Verifies API connectivity and basic functionality
"""

import os
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BotTester:
    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.api_base_url = os.getenv('API_BASE_URL')
        self.api_key = os.getenv('API_KEY')
        self.bot_username = os.getenv('BOT_USERNAME')
        
    async def test_environment_variables(self):
        """Test if all required environment variables are set"""
        print("🔍 Testing Environment Variables...")
        
        variables = {
            'TELEGRAM_BOT_TOKEN': self.telegram_token,
            'API_BASE_URL': self.api_base_url,
            'API_KEY': self.api_key,
            'BOT_USERNAME': self.bot_username
        }
        
        all_set = True
        for var_name, var_value in variables.items():
            if var_value:
                print(f"  ✅ {var_name}: {'*' * 20}")  # Hide actual values
            else:
                print(f"  ❌ {var_name}: Not set")
                all_set = False
        
        return all_set
    
    async def test_api_connectivity(self):
        """Test AhamAI API connectivity and model fetching"""
        print("\n🌐 Testing API Connectivity...")
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/v1/models", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        models = [model["id"] for model in data.get("data", [])]
                        print(f"  ✅ API Connected - {len(models)} models available")
                        print(f"  📋 Sample models: {', '.join(models[:5])}")
                        return True, models
                    else:
                        print(f"  ❌ API Error: HTTP {response.status}")
                        error_text = await response.text()
                        print(f"  📝 Error details: {error_text[:100]}...")
                        return False, []
        except Exception as e:
            print(f"  ❌ Connection Error: {e}")
            return False, []
    
    async def test_chat_completion(self, models):
        """Test chat completion with a simple message"""
        print("\n💬 Testing Chat Completion...")
        
        if not models:
            print("  ❌ No models available for testing")
            return False
        
        test_model = models[0]  # Use first available model
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in exactly 5 words."}
        ]
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": test_model,
                "messages": test_messages,
                "max_tokens": 50,
                "temperature": 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.api_base_url}/v1/chat/completions", 
                                      headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        response_text = result['choices'][0]['message']['content']
                        print(f"  ✅ Chat Completion Working")
                        print(f"  🤖 Model: {test_model}")
                        print(f"  💭 Response: {response_text[:100]}...")
                        return True
                    else:
                        error_text = await response.text()
                        print(f"  ❌ Chat Completion Error: HTTP {response.status}")
                        print(f"  📝 Error details: {error_text[:100]}...")
                        return False
        except Exception as e:
            print(f"  ❌ Chat Completion Error: {e}")
            return False
    
    async def test_telegram_bot_info(self):
        """Test Telegram bot token and get bot info"""
        print("\n🤖 Testing Telegram Bot Token...")
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{self.telegram_token}/getMe"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('ok'):
                            bot_info = data['result']
                            print(f"  ✅ Bot Token Valid")
                            print(f"  🤖 Bot Name: {bot_info.get('first_name')}")
                            print(f"  📧 Bot Username: @{bot_info.get('username')}")
                            print(f"  🆔 Bot ID: {bot_info.get('id')}")
                            return True
                        else:
                            print(f"  ❌ Telegram API Error: {data.get('description')}")
                            return False
                    else:
                        print(f"  ❌ HTTP Error: {response.status}")
                        return False
        except Exception as e:
            print(f"  ❌ Telegram Connection Error: {e}")
            return False
    
    async def test_dependencies(self):
        """Test if all required dependencies are available"""
        print("\n📦 Testing Dependencies...")
        
        dependencies = [
            'telegram',
            'aiohttp',
            'python-dotenv'
        ]
        
        all_available = True
        for dep in dependencies:
            try:
                __import__(dep.replace('-', '_'))
                print(f"  ✅ {dep}")
            except ImportError:
                print(f"  ❌ {dep} - Not installed")
                all_available = False
        
        return all_available
    
    async def run_all_tests(self):
        """Run all tests and provide summary"""
        print("🧪 AhamAI Telegram Bot Test Suite")
        print("=" * 50)
        
        results = {}
        
        # Test environment variables
        results['env'] = await self.test_environment_variables()
        
        # Test dependencies
        results['deps'] = await self.test_dependencies()
        
        # Test Telegram bot token
        results['telegram'] = await self.test_telegram_bot_info()
        
        # Test API connectivity
        api_success, models = await self.test_api_connectivity()
        results['api'] = api_success
        
        # Test chat completion if API works
        if api_success:
            results['chat'] = await self.test_chat_completion(models)
        else:
            results['chat'] = False
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 Test Summary:")
        print("=" * 50)
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            test_display = {
                'env': 'Environment Variables',
                'deps': 'Dependencies',
                'telegram': 'Telegram Bot Token',
                'api': 'AhamAI API Connection',
                'chat': 'Chat Completion'
            }
            print(f"  {status}: {test_display[test_name]}")
        
        print(f"\n🎯 Results: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed! Your bot is ready to deploy!")
            return True
        else:
            print("⚠️  Some tests failed. Please fix the issues before deploying.")
            print("\n🔧 Troubleshooting Tips:")
            if not results['env']:
                print("  • Check your .env file has all required variables")
            if not results['deps']:
                print("  • Run: pip install -r requirements.txt")
            if not results['telegram']:
                print("  • Verify your Telegram bot token from @BotFather")
            if not results['api']:
                print("  • Check your API key and base URL")
            if not results['chat']:
                print("  • Verify API permissions and model availability")
            return False

async def main():
    """Main test function"""
    tester = BotTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n🚀 Ready for deployment!")
        print("   Next steps:")
        print("   1. Push your code to GitHub")
        print("   2. Deploy on Render using the provided guide")
        print("   3. Test your bot on Telegram: @ahamai_tgbot")
    else:
        print("\n🔧 Please fix the failing tests and run again.")
    
    return success

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        exit(1)