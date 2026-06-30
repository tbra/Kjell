# pylint: disable=unused-argument

from bot import command_handler
from telegram import Update
from telegram.ext import ContextTypes
from utils import logger


@command_handler("rost", "Skapa en omröstning: /rost Fråga? | Alt1 | Alt2")
async def rost(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    if not context.args:
        await update.message.reply_text("Användning: /rost Fråga? | Alt1 | Alt2 | Alt3")
        return
    parts = [p.strip() for p in " ".join(context.args).split("|")]
    if len(parts) < 3:
        await update.message.reply_text("Du behöver en fråga och minst två alternativ separerade med |")
        return
    question = parts[0][:300]
    options = [o[:100] for o in parts[1:11]]
    await context.bot.send_poll(
        chat_id=update.message.chat_id,
        question=question,
        options=options,
        is_anonymous=False,
    )
