# pylint: disable=unused-argument

from collections import defaultdict
from datetime import timezone

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
    try:
        series = _fetch_smhi()
    except Exception:
        await update.message.reply_text("Kunde inte hämta väderdata 🌧")
        return
    entry = series[0]['data']
    temp = entry.get('air_temperature')
    wind = entry.get('wind_speed')
    symbol = int(entry.get('symbol_code') or 0)
    desc = _SYMBOLS.get(symbol, "?")
    await update.message.reply_text(f"{desc}\n🌡 {temp}°C\n💨 {wind} m/s")


def _fetch_smhi():
    url = (
        f"https://opendata-download-metfcst.smhi.se/api/category/snow1g/version/1"
        f"/geotype/point/lon/{WEATHER_LON}/lat/{WEATHER_LAT}/data.json"
    )
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()['timeSeries']


@command_handler("vader10", "10-dagarsprognos")
async def vader10(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    try:
        series = _fetch_smhi()
    except Exception:
        await update.message.reply_text("Kunde inte hämta väderdata 🌧")
        return

    from datetime import datetime
    days = defaultdict(list)
    for entry in series:
        t = datetime.fromisoformat(entry['time'].replace('Z', '+00:00')).astimezone()
        days[t.date()].append((t.hour, entry['data']))

    lines = []
    for date, entries in sorted(days.items())[:10]:
        temps = [d.get('air_temperature') for _, d in entries if d.get('air_temperature') is not None]
        # pick entry closest to noon for the symbol
        midday_data = min(entries, key=lambda x: abs(x[0] - 12))[1]
        symbol = int(midday_data.get('symbol_code') or 0)
        desc = _SYMBOLS.get(symbol, "?")
        t_min = min(temps)
        t_max = max(temps)
        day_str = date.strftime("%-d/%-m")
        lines.append(f"{day_str} {desc} {t_min:.0f}–{t_max:.0f}°C")

    await update.message.reply_text("\n".join(lines))
