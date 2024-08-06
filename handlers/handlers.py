import os
from telegram import Update
from telegram.ext import  ContextTypes, CallbackContext
import requests
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
    
async def question_command(update: Update, context: CallbackContext) -> None:
    try:
        data = {
            "topic": "python",
            "difficulty": "easy",
            "answers_num": 0
        }
        # Define headers, if required
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f'{os.getenv("SERVER_URL")}/question/generate',
            json=data,
            headers=headers
        )
        response_data = response.json()
        question = response_data.get('Question', 'No question found')
        to_return = question
        await update.message.reply_text(f"{to_return}")
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"An error occurred: {e}")


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
