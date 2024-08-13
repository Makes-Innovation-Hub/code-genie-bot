import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler
import requests
from config.CONSTANTS import DIFFICULTY_LIST

ASK_FOR_TOPIC, ASK_FOR_DIFF, ASK_FOR_NUM_ANS, USER_ANSWER = range(4)


def get_diff_keyboard():
    buttons = [KeyboardButton(diff) for diff in DIFFICULTY_LIST]
    return ReplyKeyboardMarkup(([[buttons[0], buttons[1]], [buttons[2], buttons[3]], [buttons[4]]]),
                               resize_keyboard=True,
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
    await get_question_handler(update, context)
    return USER_ANSWER


async def handle_user_answer(update: Update, context: CallbackContext):
    user_ans = update.message.text
    context.user_data['user_ans'] = user_ans
    if context.user_data['num_ans'] == 1:
        await evaluate_handler(update, context)
    return ConversationHandler.END


async def cancel_conversation(update: Update, context: CallbackContext):
    await update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END


async def get_question_handler(update: Update, context: CallbackContext) -> None:
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
        context.user_data['question_text'] = question
        await update.message.reply_text(f"{question}")
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"An error occurred: {e}")


async def evaluate_handler(update: Update, context: CallbackContext):
    try:
        body = {'user_id': str(update.message.from_user.id),
                'question_text': context.user_data['question_text'],
                'difficulty': context.user_data['difficulty'],
                'topic': context.user_data['topic'],
                'answer': context.user_data['user_ans']}

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(
            f'{os.getenv("SERVER_URL")}/question/evaluate',
            json=body,
            headers=headers
        )
        evaluation_data = response.json()
        context.user_data['evaluation_score'] = evaluation_data['Score']
        context.user_data['evaluation_expl'] = evaluation_data['Explanation']
        await update.message.reply_text(f"Your answer's score is : {context.user_data['evaluation_score']}")
        await update.message.reply_text(f"Here is the explanation : {evaluation_data['Explanation']}")
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"An error occurred: {e}")
