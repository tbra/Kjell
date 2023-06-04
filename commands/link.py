# pylint: disable=unused-argument

from bot import command_handler
from telegram import Update, constants
from telegram.ext import ContextTypes
from utils import logger


@command_handler("discord", "Länk till discord")
async def discord(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    await update.message.reply_text(text="<a href='https://discord.gg/ZN8a4uszWIP'>Discord</a>", parse_mode=constants.ParseMode.HTML)

@command_handler("github", "Länk till Kjell på github")
async def github(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    await update.message.reply_text(text="<a href='https://github.com/tbra/Kjell'>Kjellkoden</a>", parse_mode=constants.ParseMode.HTML)