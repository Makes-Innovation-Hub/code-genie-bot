import argparse
from config.config_env import create_config_env
from handlers.conversation_handler import conversation_handler_question
from handlers.basic_handlers import *
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import os
from dotenv import load_dotenv


def setup_and_load_env():
    parser = argparse.ArgumentParser()
    parser.add_argument('env', choices=['dev', 'prod'], nargs='?', default='dev')
    args = parser.parse_args()
    try:
        create_config_env(args.env)
    except Exception as e:
        raise e
        exit(1)


logger = logging.getLogger(__name__)


def main():
    try:
        setup_and_load_env()
        load_dotenv('.env')
        # Create the Application and pass it your bot's token.
        bot_token = os.getenv('BOT_TOKEN')
        if not bot_token:
            logger.error("BOT_TOKEN is not set")
            return

        # Create the Application and pass it your bot's token.
        application = ApplicationBuilder().token(bot_token).build()

        # Register command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("ip", get_public_ip_command))
        application.add_handler(CommandHandler('api', api_command))
        application.add_handler(conversation_handler_question())

        # Start the Bot
        logger.info("Starting bot", extra={"req_id": generate_request_id()})
        application.run_polling()
    except Exception as e:
        print('e: ', e)
        exit(1)


if __name__ == '__main__':
    main()
