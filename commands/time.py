# pylint: disable=unused-argument

import time
from datetime import date, datetime

import pytz
from bot import command_handler
from telegram import Update
from telegram.ext import ContextTypes
from utils import logger


@command_handler("tid", "⏲")
async def tid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    st = datetime.now().strftime("%H:%M")
    kt = datetime.now(tz=pytz.timezone('America/Toronto')).strftime("%H:%M")
    await update.message.reply_text(f"🇸🇪 - {st}\n🇨🇦 - {kt}")

@command_handler("vecka", "/vecka följt av nummer för start/slutdatum eller tomt för nuvarande")
async def vecka(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    year = date.today().year
    if context.args:
        try:
            week = int(context.args[0])
            if time.time() > datetime.timestamp(datetime.fromisocalendar(year,week,1)):
                year+=1
            message = f"{date.fromisocalendar(year,week,1)} - {date.fromisocalendar(year,week,7)}"
        except Exception:
            message = "🙅‍♀️"
    else:
        message = f"Det är vecka {date.today().strftime('%V')}"
    await update.message.reply_text(message)