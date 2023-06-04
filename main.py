from time import perf_counter

import bot
import commands
from calendar_client.sync_events import sync_calendar
from telegram import BotCommandScopeChatAdministrators, constants
from telegram.ext import ContextTypes
from utils import error, logger
from utils.constants import VERSION
from utils.secret import CHAT_ID

t1 = perf_counter()

async def alive(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Register basic and admin commands and send a message to announce that the bot is alive.
    """
    basic_commands = await application.bot.set_my_commands(command_list.get('base'))
    admin_commands = await application.bot.set_my_commands(
        command_list.get('admin') + command_list.get('base'),
        scope=BotCommandScopeChatAdministrators(chat_id=CHAT_ID),
    )
    if basic_commands:
        logger.info(("Basic commands added: %s", command_list.get('base')))
    else:
        logger.error("Commands not added")
    if admin_commands:
        logger.info(("Admin commands added: %s", command_list.get('admin')))
    else:
        logger.error("Commands not added")
    message = f"<b>Kjell V{VERSION}</b>\n<i>It's alive😱</i>"
    await context.bot.send_sticker(chat_id=CHAT_ID, sticker='CAACAgQAAxkBAAIDSGRtHKPSNN8DXICPcnp0D3gGLg8DAALiDwACQUBoU3ZMPXUD-Bb5LwQ')
    await context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=constants.ParseMode.HTML)


if __name__ == "__main__":
    application = bot.application
    command_list = bot.command_list
    t2 = perf_counter() - t1
    logger.info("Start: %s", t2)
    application.add_error_handler(error)
    job_queue = application.job_queue
    job_queue.run_once(alive, 10)
    job_queue.run_repeating(sync_calendar, interval=30)
    application.run_polling()
