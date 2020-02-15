from telegram.ext import Updater, CommandHandler
from citat import fyra_sorter as f_s
from citat import random_citat as r_c
from citat import cigg_citat as c_c
from citat import random_horse as r_h
import secrets
import requests
import re
import random
import os
import datetime

def get_qoute():
    r = requests.get('http://inspirobot.me/api?generate=true')  
    return r.text

def inspiro(bot, update):
    qoute = get_qoute()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=qoute)

def fredag(bot, update):
    chat_id = update.message.chat_id
    directory = "pics/fredag/"
    random_image = random.choice(os.listdir(directory))
    bot.send_message(chat_id=chat_id, text='Haha aa de ere')
    bot.send_photo(chat_id=chat_id, photo=open(directory+random_image, 'rb'))

def dag(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='Fredag?')
    directory = "pics/intefredag/"
    message = 'Nepp'
    if (datetime.datetime.today().weekday() == 4):
        message = 'Haha aa de ere'
        directory = "pics/fredag/"
    random_image = random.choice(os.listdir(directory))
    bot.send_message(chat_id=chat_id, text=message)
    bot.send_photo(chat_id=chat_id, photo=open(directory+random_image, 'rb'))
    
def fyra(bot, update):
    chat_id = update.message.chat_id
    message = f_s()
    bot.send_message(chat_id=chat_id, text=message)
    
def citera(bot, update):
    chat_id = update.message.chat_id
    message = r_c()
    bot.send_message(chat_id=chat_id, text=message)
    
def cigg(bot, update):
    chat_id = update.message.chat_id
    message = c_c()
    bot.send_message(chat_id=chat_id, text=message)
    
def trav(bot, update):
    chat_id = update.message.chat_id
    message = r_h()
    bot.send_message(chat_id=chat_id, text=message)

def main():
    updater = Updater(secrets.api_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('fredag',fredag))
    dp.add_handler(CommandHandler('inspiro',inspiro))
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()