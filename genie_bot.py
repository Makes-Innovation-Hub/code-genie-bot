from handlers.handlers import *
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ip", get_public_ip_command))
    application.add_handler(CommandHandler('question', question_command))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()