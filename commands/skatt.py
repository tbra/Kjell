# pylint: disable=unused-argument

from bot import message_handler
from telegram import Update
from telegram.ext import ContextTypes, filters
from utils import logger

skatter= [
    "skatt",
    "skatten",
    "skatter",
    "skatterna",
    "skattens",
    "skatters",
    "skatternas",
    "skatta",

    "alkoholskatt",
    "annonsskatt",
    "arvsskatt",
    "bilskatt",
    "energiskatt",
    "fastighetsskatt",
    "flygskatt",
    "fönsterskatt",
    "förmögenhetsskatt",
    "hundskatt",
    "inkomstskatt",
    "investeringsskatt",
    "jobbskatteavdrag",
    "kapitalskatt",
    "koldioxidskatt",
    "kupongskatt",
    "kvarskatt",
    "källskatt",
    "landstingsskatt",
    "lyxskatt",
    "meromsättningsskatt",
    "mervärdesomsättningsskatt",
    "omsättningsskatt",
    "punktskatt",
    "reklamskatt",
    "skatteavdrag",
    "skattebelopp",
    "skattebetalare",
    "skattebrott",
    "skatteexpert",
    "skatteflykt",
    "skattefordran",
    "skattefri",
    "skattefrihet",
    "skattefusk",
    "skattehöjning",
    "skatteindrivare",
    "skatteintäkt",
    "skattekontroll",
    "skattelag",
    "skattelagstiftning",
    "skattemedel",
    "skatteområde",
    "skatteparadis",
    "skattepengar",
    "skattepliktig",
    "skattepolitik",
    "skattepolitiker",
    "skattepolitisk",
    "skattereform",
    "skattesats",
    "skatteskala",
    "skattesmitare",
    "skattesänkning",
    "skattetabell",
    "skattetryck",
    "skatteverk",
    "skatteåterbäring",
    "svavelskatt",
    "tobaksskatt",
    "trängselskatt",
    "tullskatt",
    "värnskatt"
]

trigger = filters.Text(skatter) & (~filters.COMMAND)
@message_handler(trigger)
async def skatt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger message_handler %s", __name__)
    await update.message.reply_text("Skatt är stöld")
    