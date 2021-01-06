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
    
    keyboardDevices = getKeyboard(getDevices(db)) #inlineKeyboard with button taken by database's devices
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

    print(msg)
    #query_data = data value from the button; i.e="PC"
    #msg = {'id': '1568532884453601576', 'from': {'id': 365202521, 'is_bot': False, 'first_name': 'Daniele', 'username': 'DanieleTroll', 'language_code': 'it'}, 'message': {'message_id': 374, 'from': {'id': 1414329712, 'is_bot': True, 'first_name': 'DrBot', 'username': 'ProvaTrollBot'}, 'chat': {'id': 365202521, 'first_name': 'Daniele', 'username': 'DanieleTroll', 'type': 'private'}, 'date': 1609931379, 'text': 'Seleziona il dispositivo', 'reply_markup': {'inline_keyboard': [[{'text': 'PC', 'callback_data': 'PC'}], [{'text': 'Smartphone', 'callback_data': 'Smartphone'}]]}}, 'chat_instance': '7955297441696572816', 'data': 'PC'}

db = mysql.connector.connect(host="localhost", user="root", password="", database="drbot")

TOKEN = '1414329712:AAHUIof6BrcAWIBz7hgZqz_-tmXBb_lyPwI'
bot = telepot.Bot(TOKEN)

bot.message_loop({"chat": handle, "callback_query": on_callback_query})
print("Listening...")

while 1:
    time.sleep(100)