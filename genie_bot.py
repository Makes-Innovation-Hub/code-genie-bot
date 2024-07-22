from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import os
from dotenv import load_dotenv

load_dotenv()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot. How can I help you?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/ip -  get public ip"
    )
    await update.message.reply_text(help_text)

async def get_public_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get('https://api.ipify.org?format=json')
        public_ip = response.json()['ip']
        await update.message.reply_text(f'The public IP address of the bot is: {public_ip}')
        return True
    except requests.RequestException as e:
        await update.message.reply_text(f'Failed to get public IP address: {e}')
        return False

def main():
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", start))
    # Register the /help command handler
    application.add_handler(CommandHandler("help", help_command))
    # Register the /ip command handler
    application.add_handler(CommandHandler("ip", get_public_ip))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()