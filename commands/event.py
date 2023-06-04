# pylint: disable=unused-argument

from datetime import datetime, timedelta
from typing import Dict

from bot import conversation_handler
from calendar_client.authenticate_calendar import calendar_credentials
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from telegram import (ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      Update)
from telegram.ext import (ContextTypes, ConversationHandler, MessageHandler,
                          filters)
from utils import logger
from utils.secret import CALENDAR_ID

CREDENTIALS = calendar_credentials()
CALENDAR = GoogleCalendar(default_calendar=CALENDAR_ID, credentials=CREDENTIALS)
DETAILS, SUBMIT = range(2)
EVENT_KEYBOARD = [
    ["Namn"],
    ["Datum", "Start tid", "Slut tid"],
    ["Plats", "Beskrivning"],
    ["Lägg in", "Avbryt"],
]
markup = ReplyKeyboardMarkup(EVENT_KEYBOARD, one_time_keyboard=True)



def event_formatter(user_data: Dict[str, str]) -> str:
    """
    Formatera event info
    """
    data = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(data).join(["\n", "\n"])

async def event_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Ta emot textbaserad information(namn, plats, beskrivning)
    """
    text = update.message.text
    context.user_data["input"] = text
    await update.message.reply_html(
        "Ok.",
        reply_markup=ForceReply(selective=True, input_field_placeholder="Kör hårt"),
    )

    return SUBMIT

async def event_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Ta emot datuminformation(datum)
    """
    text = update.message.text
    context.user_data["input"] = text
    await update.message.reply_html(
        "Vilket datum?",
        reply_markup=ForceReply(selective=True, input_field_placeholder=datetime.today().strftime("%y%m%d")),
    )
    return SUBMIT

async def event_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Ta emot tidsinformation(starttid, sluttid)
    """
    text = update.message.text
    context.user_data["input"] = text
    await update.message.reply_html(
        "Vilken tid?",
        reply_markup=ForceReply(selective=True, input_field_placeholder=datetime.today().strftime("%H:%M")),
    )
    return SUBMIT

async def event_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Uppdatera informationen efter varje input
    """
    user_data = context.user_data
    text = update.message.text
    category = user_data["input"]
    if category in ("Start tid", "Slut tid"):
        try:
            time = datetime.strptime(text, "%H:%M")
            user_data[category] = time.time()
        except ValueError:
            await update.message.reply_text("Öhh... nej...", reply_markup=markup)
            return DETAILS
    elif category == "Datum":
        try:
            date = datetime.strptime(text, "%y%m%d")
            user_data[category] = date.date()
        except ValueError:
            await update.message.reply_text("Öhh... nej...", reply_markup=markup)
            return DETAILS
    else:
        user_data[category] = text
    del user_data["input"]

    await update.message.reply_text(
        "Ok. Så här ser det ut just nu:"
        f"{event_formatter(user_data)}Fyll i mer info, lägg in eller avbryt.",
        reply_markup=markup,
    )
    return DETAILS

async def event_submit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Rensa user_data och formatera tid och datum i start_time, finns bara datum är det ett heldagsevent.
    Kolla att det finns åtminstone ett namn och datum inlagt och lägg sen in eventet i Google Calendar.
    """
    user_data = context.user_data
    if "input" in user_data:
        del user_data["input"]
    if user_data.get('Datum') and user_data.get('Start tid'):
        start_time = datetime.combine(date=user_data.get('Datum'),time=user_data.get('Start tid'))
    else:
        start_time = user_data.get('Datum')
    if user_data.get('Namn') and start_time:
        event = Event(user_data["Namn"], start_time)
        if user_data.get('Slut tid'):
            end_time = datetime.combine(date=user_data.get('Datum'),time=user_data.get('Slut tid'))
            if end_time < start_time:
                end_time += timedelta(days=1)
            event.end = end_time
        if user_data.get('Plats'):
            event.location = user_data.get('Plats')
        if user_data.get('Beskrivning'):
            event.description = user_data.get('Beskrivning')
        try:
            CALENDAR.add_event(event)
            await update.message.reply_text("Aight", reply_markup=ReplyKeyboardRemove())
            user_data.clear()
            return ConversationHandler.END
        except Exception:
            await update.message.reply_text("Det gick inge vidare", reply_markup=markup)
    else:
        await update.message.reply_text("Du måste åtminstone fylla i namn och datum", reply_markup=markup)
    return DETAILS

async def event_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Avbryt flödet och dölj tangentbordet
    """
    user_data = context.user_data
    if "input" in user_data:
        del user_data["input"]
    await update.message.reply_text("Skit i det då", reply_markup=ReplyKeyboardRemove())
    user_data.clear()
    return ConversationHandler.END

new_event_command={
    "command": "event",
    "description": "Lägg till nytt event i kalendern",
    "admin_only": False,
}
new_event_states={
    DETAILS: [
        MessageHandler(filters.Regex("^(Namn|Plats|Beskrivning)$"), event_text),
        MessageHandler(filters.Regex("^Datum$"), event_date),
        MessageHandler(filters.Regex("^(Start tid|Slut tid)$"), event_time),
    ],
    SUBMIT: [
        MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Avbryt$")), event_update)
    ],
}
new_event_fallbacks=[
    MessageHandler(filters.Regex("^Avbryt$"), event_cancel),
    MessageHandler(filters.Regex("^Lägg in$"), event_submit)
    ]

@conversation_handler(new_event_command, new_event_states, new_event_fallbacks)
async def new_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Starta konversation för att lägga till nytt event
    """
    logger.info("%s is trying to add a new event", update.effective_user.id)
    user = update.effective_user
    await update.message.reply_html(
        rf"Fyll i all relevant information {user.mention_html()} och slutför med lägg in.",
        reply_markup=markup,
    )
    return DETAILS
