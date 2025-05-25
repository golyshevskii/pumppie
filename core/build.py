import sys
import time

from core.db.database import init_db
from core.settings import settings
from halo import Halo
from logs.logger import get_logger

logger = get_logger(__name__)


def show_logo():
    """Show logo on startup."""
    nbsp = "\u00a0"
    logo = [
        f"\n{nbsp * 8}{':' * 5}>{nbsp}{':' * 5}>",
        f"{nbsp * 7}{':' * 2}{nbsp * 2}:>{nbsp}{':' * 2}{nbsp * 2}:>",
        f"{nbsp * 6}{':' * 5}>{nbsp}{':' * 5}>",
        f"{nbsp * 5}{':' * 2}{nbsp * 5}{':' * 2}",
        f"{nbsp * 4}:{nbsp * 6}:\n",
    ]
    print("\n".join(logo))
    time.sleep(0.1)


def check_env():
    """Check if all required environment variables are set."""
    vars = ("ENV_VAR_TG_BOT_TOKEN", "ENV_VAR_DB_URL")
    for var in vars:
        if var not in settings.model_extra:
            raise ValueError(f"Environment variable {var} is not set.")


def init_agent():
    """Initialize the Agent."""
    pass


def build():
    """Build the application."""
    show_logo()

    init_message = f"Building {settings.APP_TITLE}{settings.APP_VERSION} >>>"
    if sys.stdout.isatty():
        spinner = Halo(text=init_message, spinner="dots")
        spinner.start()
    else:
        logger.info(init_message)
        spinner = None

    check_env()
    init_db()
    init_agent()

    if spinner:
        spinner.succeed("Build completed!")
        spinner.stop()


if __name__ == "__main__":
    build()
