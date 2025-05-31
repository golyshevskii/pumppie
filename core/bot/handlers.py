from core.bot.commands import start
from telegram.ext import Application, CommandHandler


def add_handlers(app: Application):
    """Add bot handlers."""
    app.add_handler(CommandHandler("start", start))

    # app.add_handler(
    #     MessageHandler((filters.TEXT | filters.VOICE | filters.AUDIO) & ~filters.COMMAND, handle_message)
    # )
    # app.add_handler(CallbackQueryHandler(handle_faq_question, pattern="^faq_"))
    # app.add_handler(CallbackQueryHandler(handle_confirm_request, pattern="^confirm_request$"))
    # app.add_handler(CallbackQueryHandler(handle_reset_request, pattern="^reset_request$"))
