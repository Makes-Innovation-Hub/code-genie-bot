import random
from telegram import InlineKeyboardButton

def get_keyboard(answers, original_answers):
    answers_lengths = [len(answer) for answer in answers]
    max_length = max(answers_lengths)

    # Determine if we should use the actual answers or numbered buttons
    if max_length > 24:
        button_labels = [str(i + 1) for i in range(len(answers))]
    else:
        button_labels = answers

    # Create the inline keyboard layout
    keyboard = []
    for i in range(0, len(answers), 2):
        row = []
        for j in range(2):
            index = i + j
            if index < len(answers):
                button_label = button_labels[index]
                callback_data = str(original_answers.index(answers[index]))
                row.append(InlineKeyboardButton(button_label, callback_data=callback_data))
        keyboard.append(row)

    return keyboard



def style_questions_answers(response_data):
    question = response_data.get('Question', 'No question found')
    answers = response_data.get('Answer', 'There is no options').copy()
    original_answers = response_data.get('Answer', 'There is no options')
    random.shuffle(answers)
    keyboard = []
    options = ""
    if len(answers) > 1:
        options = "<b>Options:</b>\n"
        keyboard = get_keyboard(answers,original_answers)
        answers_lengths = [len(answer) for answer in answers]
        if max(answers_lengths) > 24:
            for i  in range(len(answers)):
                options += f'{i+1}) ' + answers[i] + '\n'
    return [question, options, keyboard]
    