import telepot
import time
import mysql.connector
from dbManager import *
from utils import *
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

step = 1
stepPrec = 1
isHelping = False
res = []
nSolution = 0
lenRes = 0

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == "text":
        global step
        global stepPrec
        global isHelping
        global res
        global nSolution
        global lenRes

        if msg["text"] == "prova":
            bot.sendMessage(chat_id,"Seleziona il dispositivo")

db = mysql.connector.connect(host="localhost", user="root", password="", database="drbot")

TOKEN = '1414329712:AAHUIof6BrcAWIBz7hgZqz_-tmXBb_lyPwI'
bot = telepot.Bot(TOKEN)

bot.message_loop(handle)
print("Listening...")

while 1:
    time.sleep(100)