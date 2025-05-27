from core.bot.handlers import add_handlers
from core.build import build
from core.settings import settings
from logs.logger import get_logger
from telegram.ext import Application, ApplicationBuilder

logger = get_logger(__name__)


def run():
    """Run the application."""
    app: Application = ApplicationBuilder().token(settings.model_extra["ENV_VAR_TG_BOT_TOKEN"]).build()
    add_handlers(app)

    logger.info("%s.%s started → %s", settings.APP_TITLE, settings.APP_VERSION, settings.APP_URL)
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    build()
    run()
