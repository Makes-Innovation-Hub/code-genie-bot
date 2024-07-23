import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import  ContextTypes, CallbackContext
import requests

SERVER_URL = os.getenv("SERVER_URL")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot. How can I help you?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/ip -  Get public ip\n"
        "/question - Get a question from the server\n "
    )
    await update.message.reply_text(help_text)

async def get_public_ip_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        response = requests.post(f'https://code-genie-server.onrender.com/questions/generate-question/')
        print(response.json())
        await update.message.reply_text(f"Server response: {response.json()}")
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"An error occurred: {e}")

