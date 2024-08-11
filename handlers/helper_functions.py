from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

def style_questions_answers(response_data):
    question = response_data.get('Question', 'No question found')
    answers = response_data.get('Answer', 'There is no options')
    keyboard = []
    if answers != 'There is no options':
        keyboard = [
            [InlineKeyboardButton(answers[0], callback_data=answers[0]),
            InlineKeyboardButton(answers[0], callback_data=answers[0])],
            [InlineKeyboardButton(answers[0], callback_data=answers[0]),
            InlineKeyboardButton(answers[0], callback_data=answers[0])],
        ]
    
    return [question, keyboard]
    