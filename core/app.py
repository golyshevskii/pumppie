from core.build import build
from core.settings import settings

# from core.bot.command import start
# from core.bot.handler import (
#     handle_confirm_request,
#     handle_faq,
#     handle_faq_question,
#     handle_message,
#     handle_reset_request,
# )
from telegram.ext import ApplicationBuilder


def run():
    """Run the application."""
    app = ApplicationBuilder().token(settings.model_extra["ENV_VAR_TG_BOT_TOKEN"]).build()

    # app.add_handler(CommandHandler("start", start))
    # app.add_handler(MessageHandler(filters.Regex("(?i)^faq$"), handle_faq))
    # app.add_handler(
    #     MessageHandler((filters.TEXT | filters.VOICE | filters.AUDIO) & ~filters.COMMAND, handle_message)
    # )
    # app.add_handler(CallbackQueryHandler(handle_faq_question, pattern="^faq_"))
    # app.add_handler(CallbackQueryHandler(handle_confirm_request, pattern="^confirm_request$"))
    # app.add_handler(CallbackQueryHandler(handle_reset_request, pattern="^reset_request$"))

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    build()
    # run()
