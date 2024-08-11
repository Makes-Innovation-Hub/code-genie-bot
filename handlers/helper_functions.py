from telegram import InlineKeyboardButton

def switch_case(answers):
    answers_lengths = [len(answer) for answer in answers]
    if len(answers) == 2:
        return  [
                    [InlineKeyboardButton(answers[0], callback_data=answers[0]),
                    InlineKeyboardButton(answers[1], callback_data=answers[1])]
                ] if max(answers_lengths) <= 24 else [
                    [InlineKeyboardButton('1', callback_data=answers[0]),
                    InlineKeyboardButton('2', callback_data=answers[1])]
                ]
    elif len(answers) == 3:
        return  [
                    [InlineKeyboardButton(answers[0], callback_data=answers[0]),
                    InlineKeyboardButton(answers[1], callback_data=answers[1])],
                    [InlineKeyboardButton(answers[2], callback_data=answers[2])]
                ] if max(answers_lengths) <= 24 else [
                    [InlineKeyboardButton('1', callback_data=answers[0]),
                    InlineKeyboardButton('2', callback_data=answers[1])],
                    [InlineKeyboardButton('3', callback_data=answers[2])]
                ]
    elif len(answers) == 4:
        return  [
                    [InlineKeyboardButton(answers[0], callback_data=answers[0]),
                    InlineKeyboardButton(answers[1], callback_data=answers[1])],
                    [InlineKeyboardButton(answers[2], callback_data=answers[2]),
                    InlineKeyboardButton(answers[3], callback_data=answers[3])],
                ] if max(answers_lengths) <= 24 else [
                    [InlineKeyboardButton('1', callback_data=answers[0]),
                    InlineKeyboardButton('2', callback_data=answers[1])],
                    [InlineKeyboardButton('3', callback_data=answers[2]),
                    InlineKeyboardButton('4', callback_data=answers[3])],
                ]
    else:
        return "Unknown"

def style_questions_answers(response_data):
    question = response_data.get('Question', 'No question found')
    answers = response_data.get('Answer', 'There is no options')
    keyboard = []
    options = ""
    if len(answers) <= 1:
        options += 'There is no options'
    else:
        keyboard = switch_case(answers)
        answers_lengths = [len(answer) for answer in answers]
        if max(answers_lengths) > 24:
            for i  in range(len(answers)):
                options += f'{i+1}) ' + answers[i] + '\n'
    return [question, options, keyboard]
    