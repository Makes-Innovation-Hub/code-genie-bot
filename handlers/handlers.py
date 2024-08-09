import os
from telegram import Update
from telegram.ext import  ContextTypes, CallbackContext, MessageHandler, filters
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
        answer = response_data.get('Answer')
        await update.message.reply_text(f"{to_return}")
        context.user_data['correct_answer'] = answer
        context.user_data['explanations'] = response_data.get('Explanations')

        context.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_response)
        )
        

    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"An error occurred: {e}")

#this function is a message handler that waits for the user response and return the answer and the explanation
async def handle_user_response(update, context):
    user_answer = update.message.text
    correct_answer = context.user_data.get('correct_answer')
    explanations = context.user_data.get('explanations')
    correct_answer = correct_answer[0]
    explanations = explanations[0]
    await update.message.reply_text(f" the correct answer is: {correct_answer}")
    await update.message.reply_text(f"Explanation: {explanations}")
    context.application.remove_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_response)
    )





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
