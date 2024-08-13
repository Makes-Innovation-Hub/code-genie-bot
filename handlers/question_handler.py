import os
import random
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler
import requests
from config.CONSTANTS import DIFFICULTY_LIST
from handlers.helper_functions import style_questions_answers

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
    context.user_data['difficulty'] = diff if diff != 'none' else random.choice(DIFFICULTY_LIST[1:])
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
    if context.user_data['num_ans'] == 1:
        user_ans = update.message.text
        context.user_data['user_ans'] = user_ans
        await evaluate_handler(update, context)
    else:
        await closed_question_handler(update, context)
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
        context.user_data['response_data'] = response_data
        question = response_data.get('Question', 'No question found')
        await update.message.reply_text(f"{question}")
        if context.user_data['num_ans'] > 1:
            question_info = style_questions_answers(context.user_data['response_data'])
            reply_markup = InlineKeyboardMarkup(question_info[2])
            try:
                await update.message.reply_text(f"{question_info[1]}", parse_mode='HTML', reply_markup=reply_markup)
            except Exception as e:
                await update.message.reply_text(f"An error occurred: {e}")
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"An error occurred: {e}")


async def evaluate_handler(update: Update, context: CallbackContext):
    try:
        body = {'user_id': str(update.message.from_user.id),
                'question_text': context.user_data['response_data']['Question'],
                'difficulty': context.user_data['difficulty'],
                'topic': context.user_data['topic'],
                'answer': context.user_data['user_ans']
        }

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(
            f'{os.getenv("SERVER_URL")}/question/evaluate',
            json=body,
            headers=headers, params={'ai_answer': context.user_data['response_data']['Answer'][0]}
        )
        evaluation_data = response.json()
        context.user_data['evaluation_score'] = evaluation_data['Score']
        context.user_data['evaluation_expl'] = evaluation_data['Explanation']
        await update.message.reply_text(f"Your answer's score is : {context.user_data['evaluation_score']}")
        await update.message.reply_text(f"Here is the explanation : {evaluation_data['Explanation']}")
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"An error occurred: {e}")


async def closed_question_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Retrieve the response_data stored in question_command
    response_data = context.user_data.get('response_data')

    if not response_data:
        await query.edit_message_text(text="Error: No data found for this question.")
        return ConversationHandler.END

    # Check if the selected answer is correct
    correct_answer = '0'  # Assuming the first answer is the correct one
    selected_answer = query.data
    explanation = response_data.get('Explanations', 'No explanation available.')

    if selected_answer == correct_answer:
        feedback = "Correct! 🎉"
    else:
        feedback = f"Incorrect. The correct answer was: {response_data['Answer'][0]}"

    # Include the explanation in the feedback
    feedback_with_explanation = f"{feedback}\n\nExplanation: {explanation[0]}"

    await query.edit_message_text(
        text=f"Selected option: {response_data['Answer'][int(selected_answer)]}\n\n{feedback_with_explanation}")
    try:
        answer_correct = selected_answer == correct_answer
        body = {'user_id': str(update.effective_user.id),
                'question_text': context.user_data['response_data']['Question'],
                'topic': context.user_data['topic'],
                'difficulty': context.user_data['difficulty'],
                'answer_correct': answer_correct,
                'score': 10 if answer_correct else 0,
                'answer': response_data['Answer'][int(selected_answer)],
                }

        response = requests.post(
            f'{os.getenv("SERVER_URL")}/users/add-user-stats',
            data=body
        )
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"An error occurred: {e}")
    return ConversationHandler.END
