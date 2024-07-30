import logging
import argparse
from config.config_env import create_config_env
from handlers.handlers import *
from telegram.ext import ApplicationBuilder, CommandHandler
import os
from dotenv import load_dotenv
from config.logging_config import logging, generate_request_id


def setup_and_load_env():
    parser = argparse.ArgumentParser()
    parser.add_argument('env', choices=['dev', 'prod'], nargs='?', default='dev')
    args = parser.parse_args()
    try:
        create_config_env(args.env)
    except Exception as e:
        raise e
        exit(1)


# Initialize the logger
logger = logging.getLogger(__name__)

def main():
    setup_and_load_env()
    load_dotenv('.env')
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN is not set")
        return
      
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(bot_token).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", start_command))
    # Register the /help command handler
    application.add_handler(CommandHandler("help", help_command))
    # Register the /ip command handler
    application.add_handler(CommandHandler("ip", get_public_ip_command))
    # Register the /api command handler
    application.add_handler(CommandHandler('api', api_command))
    
    # Start the Bot
    logger.info("Starting bot", extra={"req_id": generate_request_id()})
    application.run_polling()

if __name__ == '__main__':
    main()
