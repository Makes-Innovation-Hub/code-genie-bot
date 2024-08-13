from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from .question_handler import *


def conversation_handler_question():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("question", start_conversation)],
        states={
            ASK_FOR_TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_topic)],
            ASK_FOR_DIFF: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_diff)],
            ASK_FOR_NUM_ANS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_num_ans)],
            USER_ANSWER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_answer),
                CallbackQueryHandler(closed_question_handler)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
        per_message=False
    )
    return conv_handler
