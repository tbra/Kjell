from bot import command_handler
from telegram import Update
from telegram.ext import ContextTypes
from utils import logger


@command_handler("pin", "Pinna föregående meddelande eller svara /pin på ett meddelande")
async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    await update.message.reply_text("k📌")
    try:
        message = update.message.reply_to_message.message_id
    except Exception:
        message = update.message.message_id-1
    await context.bot.pin_chat_message(chat_id=update.message.chat_id, message_id=message)