# pylint: disable=unused-argument

import requests
from bot import command_handler
from telegram import Update
from telegram.ext import ContextTypes
from utils import logger
from utils.constants import WEATHER_LAT, WEATHER_LON

_SYMBOLS = {
    1: "☀️ Klart", 2: "🌤 Mest klart", 3: "⛅️ Variabel molnighet",
    4: "🌥 Halvklart", 5: "☁️ Molnigt", 6: "☁️ Mulet", 7: "🌫 Dimma",
    8: "🌦 Lätta regnskurar", 9: "🌧 Måttliga regnskurar", 10: "🌧 Kraftiga regnskurar",
    11: "⛈ Åskväder", 12: "🌨 Snöblandade skurar", 13: "🌨 Snöblandade skurar",
    14: "🌨 Kraftiga snöblandade skurar", 15: "🌨 Lätta snöbyar", 16: "❄️ Måttliga snöbyar",
    17: "❄️ Kraftiga snöbyar", 18: "🌧 Lätt regn", 19: "🌧 Måttligt regn",
    20: "🌧 Kraftigt regn", 21: "⛈ Åska", 22: "🌨 Lätt snöblandat regn",
    23: "🌨 Måttligt snöblandat regn", 24: "🌨 Kraftigt snöblandat regn",
    25: "❄️ Lätt snöfall", 26: "❄️ Måttligt snöfall", 27: "❄️ Kraftigt snöfall",
}


@command_handler("vader", "Aktuellt väder")
async def vader(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    url = (
        f"https://opendata-download-metfcst.smhi.se/api/category/snow1g/version/1"
        f"/geotype/point/lon/{WEATHER_LON}/lat/{WEATHER_LAT}/data.json"
    )
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        await update.message.reply_text("Kunde inte hämta väderdata 🌧")
        return
    data = response.json()
    entry = data['timeSeries'][0]['data']
    temp = entry.get('air_temperature')
    wind = entry.get('wind_speed')
    symbol = int(entry.get('symbol_code') or 0)
    desc = _SYMBOLS.get(symbol, "?")
    await update.message.reply_text(f"{desc}\n🌡 {temp}°C\n💨 {wind} m/s")
