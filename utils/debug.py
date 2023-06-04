import html
import json
import logging
import traceback

import utils.constants as const
from telegram import Update, constants
from telegram.ext import ContextTypes
from utils.secret import DEBUG_CHAT_ID

### LOGGING
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=const.LOG_LEVEL
)
logger = logging.getLogger(__name__)

### ERRORS
error_message = "No errors"

async def error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    global error_message
    error_message = f"<pre>{html.escape(tb_string)}</pre>"
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    await update.message.reply_text("Något gick fel")
    await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text=message, parse_mode=constants.ParseMode.HTML)

def get_latest_error() -> str:
    return error_message
