from telegram.ext import Updater, CommandHandler
import secrets
import requests
import re
import random
import os

def get_qoute():
    r = requests.get('http://inspirobot.me/api?generate=true')  
    return r.text

def inspiro(bot, update):
    qoute = get_qoute()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=qoute)

def fredag(bot, update):
    chat_id = update.message.chat_id
    directory = "pics/"
    random_image = random.choice(os.listdir(directory))
    bot.send_message(chat_id=chat_id, text='Haha aa de ere')
    bot.send_photo(chat_id=chat_id, photo=open('pics/'+random_image, 'rb'))

def main():
    updater = Updater(secrets.api_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('fredag',fredag))
    dp.add_handler(CommandHandler('inspiro',inspiro))
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()