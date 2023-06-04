# pylint: disable=unused-argument

from bot import command_handler
from telegram import Update
from telegram.ext import ContextTypes
from utils import logger
from utils.constants import VERSION
from utils.secret import CHAT_ID


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

@command_handler("chat", "Skicka ett meddelande som Kjell eller svara /chat på en gif för att skicka den", 1)
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    if context.args:
        message = ' '.join(context.args)
        await context.bot.send_message(chat_id=CHAT_ID, text=message)
        return
    try:
        animation = update.message.reply_to_message.animation.file_id
        await context.bot.send_animation(chat_id=CHAT_ID, animation=animation)
    except AttributeError:
        await update.message.reply_text('Gör om gör rätt')
