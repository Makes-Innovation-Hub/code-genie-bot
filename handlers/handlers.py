import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  ContextTypes, CallbackContext
import requests
from config import CONSTANTS
from handlers.helper_functions import *


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
            "answers_num": 3
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
        while(data["answers_num"] != len(response_data.get('Answer', 'There is no options'))):
            response = requests.post(
                f'{os.getenv("SERVER_URL")}/question/generate',
                json=data,
                headers=headers
            )   
        context.user_data['response_data'] = response_data
        to_return = style_questions_answers(response_data)
        reply_markup = InlineKeyboardMarkup(to_return[2])
        await update.message.reply_text(f"{to_return[0]}")
        await update.message.reply_text(f"{to_return[1]}", parse_mode='HTML', reply_markup=reply_markup)
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


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Retrieve the response_data stored in question_command
    response_data = context.user_data.get('response_data')

    if not response_data:
        await query.edit_message_text(text="Error: No data found for this question.")
        return

    # Check if the selected answer is correct
    correct_answer = response_data['Answer'][0]  # Assuming the first answer is the correct one
    selected_answer = query.data
    explanation = response_data.get('Explanations', 'No explanation available.')

    if selected_answer == correct_answer:
        feedback = "Correct! 🎉"
    else:
        feedback = f"Incorrect. The correct answer was: {correct_answer}"

    # Include the explanation in the feedback
    feedback_with_explanation = f"{feedback}\n\nExplanation: {explanation[0]}"

    await query.edit_message_text(text=f"Selected option: {selected_answer}\n\n{feedback_with_explanation}")

