# pylint: disable=no-member

import os
import pickle
from datetime import datetime

from dateutil.parser import parse
from telegram import constants
from telegram.ext import ContextTypes
from utils.secret import CALENDAR_ID, CHAT_ID

from .authenticate_calendar import calendar_service


def sync_events():
    """
    Checks if there are new events in the calendar and returns them.
    Uses the sync_token.pickle file to only get changes since the last sync.
    """
    calendar = calendar_service()
    sync_token = None
    if os.path.exists('sync_token.pickle'):
        with open('sync_token.pickle', 'rb') as token:
            sync_token = pickle.load(token)
    if not sync_token:
        events_result = calendar.events().list(calendarId=CALENDAR_ID).execute()
    else:
        events_result = calendar.events().list(calendarId=CALENDAR_ID, syncToken=sync_token).execute()
    events = events_result.get('items', [])
    if not events:
        return None
    new_sync_token = events_result.get('nextSyncToken')
    if new_sync_token:
        with open('sync_token.pickle', 'wb') as token:
            pickle.dump(new_sync_token, token)
    return events


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
