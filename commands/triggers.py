# pylint: disable=unused-argument

import random

from bot import message_handler
from commands.random import citat_list
from telegram import ReactionTypeEmoji, Update
from telegram.ext import ContextTypes, filters
from utils import logger

_REACTION_EMOJIS = [
    "👍", "👎", "❤", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱",
    "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡",
    "🥱", "🥴", "😍", "🐳", "❤️‍🔥", "🌚", "🌭", "💯", "🤣", "⚡",
    "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈",
    "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨",
    "🤝", "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿",
    "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂️",
    "🤷", "🤷‍♀️", "😡",
]


@message_handler(filters.Regex(r'(?i)\bkjell\b') & ~filters.COMMAND)
async def kjell_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Trigger message_handler %s", __name__)
    await update.message.reply_text(random.choice(citat_list))


@message_handler(~filters.COMMAND)
async def random_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if random.random() >= 0.01:
        return
    emoji = random.choice(_REACTION_EMOJIS)
    try:
        await update.message.set_reaction([ReactionTypeEmoji(emoji=emoji)])
    except Exception:
        pass
