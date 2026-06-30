# pylint: disable=no-member

import os
import pickle
from datetime import datetime

from dateutil.parser import parse
from telegram import constants
from telegram.ext import ContextTypes
from utils.secret import CALENDAR_ID, CHAT_ID
from utils import logger

from .authenticate_calendar import calendar_service


def sync_events():
    """
    Checks if there are new events in the calendar and returns them.
    Uses the sync_token.pickle file to only get changes since the last sync.
    """
    calendar = calendar_service()
    sync_token = 'init'
    if os.path.exists('sync_token.pickle'):
        with open('sync_token.pickle', 'rb') as token:
            sync_token = pickle.load(token)
    logger.info(f"Old syncToken: {sync_token}, loaded from storage")
    try:
        logger.info("Trying incremental sync")
        events_result = calendar.events().list(calendarId=CALENDAR_ID, syncToken=sync_token).execute()
        events = events_result.get('items', [])
    except:
        logger.info("Incremental sync failed")
        events_result = calendar.events().list(calendarId=CALENDAR_ID).execute()
        events = None
    new_sync_token = events_result.get('nextSyncToken')
    if new_sync_token:
        logger.info(f"New syncToken: {new_sync_token}, saved to storage")
        with open('sync_token.pickle', 'wb') as token:
            pickle.dump(new_sync_token, token)
    if events:
        logger.info(f"Events: {events}")
        return events
    return None


async def sync_calendar(context: ContextTypes.DEFAULT_TYPE):
    """
    If there are any changes in the calendar, send a message to the chat.
    Sends a different message depending on the status of the event.
    """
    changes = sync_events()
    if changes:
        for event in changes:
            info = []
            summary = ""
            if event['status'] == 'cancelled':
                await context.bot.send_message(chat_id=CHAT_ID, text="Inställt event!🗑❌")
            else:
                created = datetime.timestamp(parse(event['created']))
                updated = datetime.timestamp(parse(event['updated']))
                summary = f"<i>{event['summary']}</i>"
                if updated-created<5:
                    status = "Nytt event!🎈🎷"
                else:
                    status = "Uppdaterat event!✒🔃"
                if event['start'].get('dateTime'):
                    start = parse(event['start'].get('dateTime'))
                    end = parse(event['end'].get('dateTime'))
                    info.append(f"📆{start.strftime('%F')}")
                    info.append(f"🕒{start.strftime('%H:%M')}-{end.strftime('%H:%M')}")
                else:
                    info.append(f"📆{event['start'].get('date')}")
                if event.get('location'):
                    info.append(f"📍{event['location']}") 
                if event.get('description'):
                    info.append(f"ℹ{event['description']}") 
                message = f"{summary}\n<code>\n{chr(10).join(info)}</code>"
                await context.bot.send_message(
                    chat_id=CHAT_ID, text=f"<b>{status}</b>", 
                    parse_mode=constants.ParseMode.HTML
                    )
                await context.bot.send_message(
                    chat_id=CHAT_ID, text=message, 
                    parse_mode=constants.ParseMode.HTML
                    )
