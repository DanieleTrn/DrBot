import telepot
import time
import mysql.connector
from dbManager import *


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == "text":
        print("ciao")

db = mysql.connector.connect(host="localhost", user="root", password="", database="drbot")

TOKEN = '1414329712:AAHUIof6BrcAWIBz7hgZqz_-tmXBb_lyPwI'
bot = telepot.Bot(TOKEN)

bot.message_loop(handle)

print("Listening...")

while 1:
    time.sleep(100)