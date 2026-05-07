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

from urllib.parse import urlparse

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "👋 <b>Store Link Updater</b>\n\n"
        "Send the <b>Current URL</b> (or just the domain) and the <b>Affiliate Link</b>.\n\n"
        "Format: <code>[url/domain] [affiliate_link]</code>\n"
        "Example: <code>amazon.in https://amzn.to/xyz</code>\n"
        "Example: <code>https://www.flipkart.com/item https://fktr.in/abc</code>\n\n"
        "✅ I will automatically find the store and update it.\n"
        "❌ If the store doesn't exist, I will give an error."
    )
    bot.reply_to(message, help_text, parse_mode='HTML')

def extract_domain(text):
    # If it's a URL, extract netloc
    if text.startswith("http"):
        domain = urlparse(text).netloc
    else:
        domain = text
    # Remove www. and cleanup
    return domain.lower().replace("www.", "").split('/')[0].strip()

@bot.message_handler(func=lambda message: True)
def handle_update(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "❌ <b>Invalid Format</b>\nPlease send: <code>domain affiliate_link</code>", parse_mode='HTML')
            return

        # Extract domain from first part (handles full URLs too)
        domain = extract_domain(parts[0])
        new_url = parts[1]

        if not new_url.startswith("http"):
            bot.reply_to(message, "❌ <b>Invalid Affiliate Link</b>\nLink must start with http or https.")
            return

        bot.send_chat_action(message.chat.id, 'typing')
        result = update_affiliate_link(JSON_PATH, domain, new_url)

        if result["status"] == "success":
            bot.reply_to(message, f"✅ <b>Updated {domain}</b>\n{result['message']}", parse_mode='HTML')
        else:
            # Combined error and warning for simplicity
            bot.reply_to(message, f"❌ <b>Failed to update {domain}</b>\n{result['message']}", parse_mode='HTML')

    except Exception as e:
        bot.reply_to(message, f"⚠️ <b>Error:</b> {str(e)}", parse_mode='HTML')

if __name__ == "__main__":
    print("Bot is starting...")
    bot.infinity_polling()
