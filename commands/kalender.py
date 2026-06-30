# pylint: disable=unused-argument

from datetime import datetime, timedelta

from bot import command_handler
from calendar_client.authenticate_calendar import calendar_credentials
from gcsa.google_calendar import GoogleCalendar
from telegram import Update, constants
from telegram.ext import ContextTypes
from utils import logger
from utils.secret import CALENDAR_ID

_calendar = None


def _get_calendar() -> GoogleCalendar:
    global _calendar
    if _calendar is None:
        _calendar = GoogleCalendar(default_calendar=CALENDAR_ID, credentials=calendar_credentials())
    return _calendar


@command_handler("kalender", "Kommande händelser i kalendern")
async def kalender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    try:
        cal = _get_calendar()
        now = datetime.now()
        events = list(cal.get_events(
            time_min=now,
            time_max=now + timedelta(days=60),
            order_by='startTime',
            single_events=True,
        ))[:5]
        if not events:
            await update.message.reply_text("Inga kommande händelser 📭")
            return
        lines = []
        for event in events:
            start = event.start
            date_str = start.strftime("%d/%m %H:%M") if isinstance(start, datetime) else start.strftime("%d/%m")
            lines.append(f"📅 <b>{event.summary}</b> – <code>{date_str}</code>")
        await update.message.reply_text("\n".join(lines), parse_mode=constants.ParseMode.HTML)
    except Exception as e:
        logger.error("Kalender error: %s", e)
        await update.message.reply_text("Kunde inte hämta kalendern 😢")
