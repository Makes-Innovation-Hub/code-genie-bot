import os
import requests
from telegram import Update
from telegram.ext import ContextTypes

from config import CONSTANTS


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot. How can I help you?')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(CONSTANTS.HELP_COMMAND_TEXT)


async def get_public_ip_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        response = requests.get('https://api.ipify.org?format=json')
        public_ip = response.json()['ip']
        await update.message.reply_text(f'The public IP address of the bot is: {public_ip}')
        return True
    except requests.RequestException as e:
        await update.message.reply_text(f'Failed to get public IP address: {e}')
        return False


async def api_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(os.getenv("SERVER_URL"))
        response.raise_for_status()
        data = response.json()
        await update.message.reply_text(data)
    except requests.RequestException as e:
        await update.message.reply_text(f"Request failed: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"An unexpected error occurred: {str(e)}")
