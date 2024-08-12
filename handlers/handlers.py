import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler
import requests
from config import CONSTANTS
from config.CONSTANTS import DIFFICULTY_LIST

ASK_FOR_TOPIC, ASK_FOR_DIFF, ASK_FOR_NUM_ANS = range(3)


def get_diff_keyboard():
    buttons = [KeyboardButton(diff) for diff in DIFFICULTY_LIST]
    return ReplyKeyboardMarkup(([[buttons[0], buttons[1]], [buttons[2], buttons[3]], [buttons[4]]]), resize_keyboard=True,
                               one_time_keyboard=True)


def get_num_ans_keyboard():
    buttons = [str(i) for i in range(1, 5)]
    return ReplyKeyboardMarkup(([[buttons[0], buttons[1]], [buttons[2], buttons[3]]]), resize_keyboard=True,
                               one_time_keyboard=True)


async def start_conversation(update: Update, context: CallbackContext):
    await update.message.reply_text("Please provide a topic for the question:")
    return ASK_FOR_TOPIC


async def handle_topic(update: Update, context: CallbackContext):
    topic = update.message.text
    context.user_data['topic'] = topic
    await update.message.reply_text(f"Please provide a difficulty from following options {DIFFICULTY_LIST}:",
                                    reply_markup=get_diff_keyboard())
    return ASK_FOR_DIFF


async def handle_diff(update: Update, context: CallbackContext):
    diff = update.message.text
    if diff not in DIFFICULTY_LIST:
        await update.message.reply_text(
            f"Invalid difficulty, please make sure to choose from following options {DIFFICULTY_LIST}")
        return ASK_FOR_DIFF
    context.user_data['difficulty'] = diff
    await update.message.reply_text("Please provide the number of answers (FROM 1-4):",
                                    reply_markup=get_num_ans_keyboard())
    return ASK_FOR_NUM_ANS


async def handle_num_ans(update: Update, context: CallbackContext):
    num_ans = update.message.text
    if not num_ans.isdigit() or int(num_ans) <= 0 or int(num_ans) > 4:
        await update.message.reply_text(
            f"Invalid number of answers, please make sure to choose a number from 1-4:")
        return ASK_FOR_NUM_ANS
    context.user_data['num_ans'] = int(num_ans)
    await question_command(update, context)


async def cancel_conversation(update: Update, context: CallbackContext):
    await update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END


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
            "topic": context.user_data['topic'],
            "difficulty": context.user_data['difficulty'],
            "answers_num": context.user_data['num_ans']
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
