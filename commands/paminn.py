# pylint: disable=unused-argument

import re

from bot import command_handler
from telegram import Update, constants
from telegram.ext import ContextTypes
from utils import logger

_TIME_RE = re.compile(r'^(\d+)(m|h|d)$')
_UNITS = {'m': 60, 'h': 3600, 'd': 86400}


@command_handler("paminn", "Sätt en påminnelse: /paminn 30m Köp mjölk")
async def paminn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Användning: /paminn <tid> <meddelande>\nEx: /paminn 30m Köp mjölk")
        return
    match = _TIME_RE.match(context.args[0])
    if not match:
        await update.message.reply_text("Ogiltig tid. Använd t.ex. 30m, 2h, 1d")
        return
    seconds = int(match.group(1)) * _UNITS[match.group(2)]
    text = " ".join(context.args[1:])
    chat_id = update.message.chat_id
    user = update.effective_user.mention_html()

    async def _callback(ctx: ContextTypes.DEFAULT_TYPE) -> None:
        await ctx.bot.send_message(
            chat_id=chat_id,
            text=f"⏰ Påminnelse för {user}: {text}",
            parse_mode=constants.ParseMode.HTML,
        )

    context.job_queue.run_once(_callback, seconds)
    await update.message.reply_text(f"⏰ Påminnelse satt om {context.args[0]}!")
