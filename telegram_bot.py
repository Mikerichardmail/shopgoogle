import telebot
import json
import os
from dotenv import load_dotenv
from update_store_link import update_affiliate_link

# Load credentials from .env file
load_dotenv()

# Get token from environment
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(API_TOKEN)
JSON_PATH = "app/src/main/assets/stores_data.json"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "👋 Welcome to the Store Link Updater Bot!\n\n"
        "To update a store's affiliate link, send a message in this format:\n"
        "<code>domain link</code>\n\n"
        "Example:\n"
        "<code>amazon.in https://amzn.to/your-id</code>\n\n"
        "I will check if the store exists and update it for you."
    )
    bot.reply_to(message, help_text, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def handle_update(message):
    try:
        # Split message into domain and link
        parts = message.text.split()
        
        if len(parts) != 2:
            bot.reply_to(message, "❌ Invalid format. Please send: <code>domain link</code>", parse_mode='HTML')
            return

        domain = parts[0]
        new_url = parts[1]

        # Call the update logic
        bot.send_chat_action(message.chat.id, 'typing')
        result = update_affiliate_link(JSON_PATH, domain, new_url)

        if result["status"] == "success":
            bot.reply_to(message, f"🚀 <b>Live Update Success!</b>\n{result['message']}", parse_mode='HTML')
        elif result["status"] == "warning":
            bot.reply_to(message, f"⚠️ <b>Partial Success:</b>\n{result['message']}", parse_mode='HTML')
        else:
            bot.reply_to(message, f"❌ <b>Error:</b>\n{result['message']}", parse_mode='HTML')

    except Exception as e:
        bot.reply_to(message, f"⚠️ An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    print("Bot is starting...")
    bot.infinity_polling()
