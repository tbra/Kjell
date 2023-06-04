# pylint: disable=unused-argument

from bot import command_handler
from telegram import Update, constants
from telegram.ext import ContextTypes
from utils import get_latest_error, logger


@command_handler("message", "Svarar med info om meddelandet", 1)
async def message_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    await update.message.reply_text(update)

@command_handler("get_commands", "Lista tillgängliga kommandon", 1)
async def get_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    commands = await context.bot.get_my_commands()
    await update.message.reply_text(commands)

@command_handler("set_default_commands", "Skriv över alla kommandon med default", 1)
async def set_default_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    new_commands = [
        ("test", "Inga kommandon registrerade"),
    ]
    set_commands = await context.bot.set_my_commands(new_commands)
    await update.message.reply_text(set_commands)

@command_handler("test", "Svarar med info om användaren, /test error simulerar ett exception", 1)
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    if context.args and context.args[0] == 'error':
        raise Exception("Ett testfel")
    else:
        user = update.effective_user
        await update.message.reply_text(user)

@command_handler("error", "Det senaste felmeddelandet", 1)
async def last_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    message = get_latest_error()
    await update.message.reply_text(message, parse_mode=constants.ParseMode.HTML)