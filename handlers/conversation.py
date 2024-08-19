from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters
from handlers.handlers import *


def conversation_handler_question():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("question", start_conversation)],
        states={
            ASK_FOR_TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_topic)],
            ASK_FOR_DIFF: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_diff)],
            ASK_FOR_NUM_ANS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_num_ans)]
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )
    return conv_handler

def getting_api_details():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create', create_challenge)],
        states={
            ASK_FOR_API_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, GET_API_ID)],
            ASK_FOR_API_HASH: [MessageHandler(filters.TEXT & ~filters.COMMAND, GET_API_HASH)],
            ASK_FOR_PHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, GET_PHONE_NUMBER)],
        },
        fallbacks=[CommandHandler('cancel', cancel_conversation)],
    )
