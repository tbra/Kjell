# pylint: disable=unused-argument

from datetime import date, datetime

import requests
from bot import command_handler
from telegram import Update
from telegram.ext import ContextTypes
from utils import logger


@command_handler("elpris", "Nuvarande och nästa timmes elpris")
async def el_pris(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    date_str = date.today().strftime("%Y/%m-%d")
    url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_str}_SE4.json"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        current_hour = datetime.now().hour
        next_hour = (current_hour + 1) % 24
        sek_per_kwh_values = []
        for obj in data:
            time_start = datetime.fromisoformat(obj['time_start']).hour
            time_end = datetime.fromisoformat(obj['time_end']).hour
            if (time_start <= current_hour < time_end) or (time_start <= next_hour < time_end):
                sek_per_kwh_values.append(obj['SEK_per_kWh'])
        if len(sek_per_kwh_values) > 0:
            message = "Elpris för nuvarande och nästa timme:\n"
            message += f"Nu: {sek_per_kwh_values[0]}:-\n"
            message += f"Nästa timme: {sek_per_kwh_values[1]}:-\n"
        else:
            message = "Inget elpris hittades för den nuvarande och nästa timme."
        await update.message.reply_text(message)
    else:
        message = f"Fel vid API-anropet. Statuskod: {response.status_code}"
        await update.message.reply_text(message)

@command_handler("inspiro", "Inspirera mig senpai😳")
async def inspiro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    message = requests.get('http://inspirobot.me/api?generate=true', timeout=10)
    await update.message.reply_photo(message.text)

@command_handler("epic", "Gratis på Epic Store just nu")
async def epic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger command_handler %s", __name__)
    url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        games = response.json()['data']['Catalog']['searchStore']['elements']
        valid_games = [game for game in games if "Mystery Game" not in game['title']]

        if valid_games:
            message = "Nuvarande gratis spel på Epic Store:\n"
            for game in valid_games:
                title = game['title']
                description = game['description']
                image_url = game['keyImages'][0]['url'] if game['keyImages'] else None
                link = f"https://www.epicgames.com/store/en-US/p/{game['productSlug']}" if game['productSlug'] else None
                end_date_str = game['expiryDate']

                end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%S.%fZ") if end_date_str else None
                remaining_time = f"\nGratis till: {end_date.strftime('%Y-%m-%d %H:%M')}" if end_date else ""

                game_info = f"*{title}*\n"
                if description:
                    game_info += f"{description}\n"
                if end_date_str:
                    game_info += f"{remaining_time}\n".replace('-', '\\-')
                if link:
                    game_info += f"[Läs mer och hämta här]({link})\n\n"
                message += game_info

            if image_url:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=message, parse_mode='MarkdownV2')
        else:
            message = "Inga gratis spel tillgängliga just nu."
            await update.message.reply_text(message)
    else:
        message = "Ett fel uppstod vid hämtning av spelinformationen från Epic Store."
        await update.message.reply_text(message)