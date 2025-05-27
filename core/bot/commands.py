from core.bot.menu import set_menu
from core.bot.messages import get, msg
from logs.logger import get_logger
from telegram import Update
from telegram.ext import ContextTypes

logger = get_logger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respond to /start command."""
    user_id = update.effective_user.id
    username = update.effective_user.username
    logger.debug("User %(username)s (%(user_id)s) started the bot", {"username": username, "user_id": user_id})

    reply_markup = await set_menu()
    await update.message.reply_text(get(msg.COMMAND_START), reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respond to /help command."""
    await update.message.reply_text(get(msg.COMMAND_HELP))
