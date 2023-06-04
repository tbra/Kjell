# pylint: disable=unused-argument

from typing import Any, Callable, Dict, List

from bot.application import application
from telegram import Update
from telegram.ext import (BaseHandler, CommandHandler, ConversationHandler,
                          MessageHandler, filters)
from utils import logger

command_list = {
    'base' : [],
    'admin' : [],
    }

def command_handler(command: str, description: str = None, admin_only: bool = False):
    """
    Register a command handler, with optional description and admin status.
    """
    logger.info("Adding command: %s, description: %s, admin: %s", command, description, admin_only)
    def decorator(func: Callable) -> Callable:
        handler = CommandHandler(command, func)
        application.add_handler(handler)
        if description:
            if not admin_only:
                command_list.get('base').append((command, description))
            else:
                command_list.get('admin').append((command, description))
        return func
    return decorator

def message_handler(trigger: filters.BaseFilter):
    """
    Register a message handler.
    """
    logger.info("Listening for messages using filter: %s", trigger)
    def decorator(func: Callable) -> Callable:
        handler = MessageHandler(trigger, func)
        application.add_handler(handler)
        return func
    return decorator

def conversation_handler(
        commands: Dict[str, str], 
        states: Dict[object, List[BaseHandler[Update, Any]]],
        fallbacks: List[BaseHandler[Update, Any]], 
        **kwargs):
    """
    Register a conversation handler.
    """
    print(type(commands), commands)
    print(type(states), states)
    print(type(fallbacks), fallbacks)
    logger.info(
        "Adding ConversationHandler with commands: %s, states: %s, and fallbacks: %s",
        commands, states, fallbacks
        )
    def decorator(func: Callable) -> Callable:
        command = commands.get('command')
        entry_points = [CommandHandler(command, func)]
        print(type(entry_points), entry_points)
        print(type(states), states)
        print(type(fallbacks), fallbacks)
        handler = ConversationHandler(entry_points, states, fallbacks)
        application.add_handler(handler)
        if commands.get('description'):
            if not commands.get('admin_only'):
                command_list.get('base').append((command, commands.get('description')))
            else:
                command_list.get('admin').append((command, commands.get('description')))
        return func
    return decorator
