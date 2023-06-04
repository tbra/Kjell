# pylint: disable=unused-argument

from bot import command_handler
from telegram import Update
from telegram.ext import ContextTypes
from utils import logger
from utils.constants import VERSION


@command_handler("start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    user = update.effective_user
    await update.message.reply_html(rf"Hej {user.mention_html()}!")

@command_handler("version", "???")
async def version(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    await update.message.reply_text(VERSION)

@command_handler("changelog")
async def changelog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    await update.message.reply_text('Lite allt möjligt')
