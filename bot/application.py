from telegram.ext import Application
from utils.secret import API_TOKEN

application = Application.builder().token(API_TOKEN).build()
