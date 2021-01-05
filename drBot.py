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

    #keyboard = InlineKeyboardMarkup(inline_keyboard= [
               #[InlineKeyboardButton(text="Cliccami",callback_data="press")],
                #])
    
    keyboardDevices = getKeyboard(getDevices(db))

    if content_type == "text":
        global step
        global stepPrec
        global isHelping
        global res
        global nSolution
        global lenRes

        if msg["text"] == "prova":
            print(keyboardDevices)
            bot.sendMessage(chat_id,"Seleziona il dispositivo", reply_markup=keyboardDevices)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")

    bot.answerCallbackQuery(query_id,text="Yeah")

db = mysql.connector.connect(host="localhost", user="root", password="", database="drbot")

TOKEN = '1414329712:AAHUIof6BrcAWIBz7hgZqz_-tmXBb_lyPwI'
bot = telepot.Bot(TOKEN)

bot.message_loop({"chat": handle, "callback_query": on_callback_query})
print("Listening...")

while 1:
    time.sleep(100)