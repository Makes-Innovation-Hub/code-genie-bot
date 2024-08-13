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
