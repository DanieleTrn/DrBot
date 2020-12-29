import telepot
import time
import mysql.connector
from dbManager import *
#from botCommands import *

step = 1
sintomo = ""
soluzione = ""
stepDB = 0
isTecnico = False

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == "text":
        global step
        global sintomo
        global soluzione
        global stepDB
        global isTecnico

        if msg['text'] == "aggiungi" or msg['text'] == "Aggiungi":
            if step == 1:
                bot.sendMessage(chat_id,"Inserisci il sintomo")
                step = 2
        elif step == 2:
            sintomo = msg['text']
            bot.sendMessage(chat_id,"Inserisci la soluzione")
            step = 3
        elif step == 3:
            soluzione = msg['text']
            bot.sendMessage(chat_id,"Inserisci lo step")
            step = 4
        elif step == 4:
            stepDB = msg['text']
            bot.sendMessage(chat_id,"E' un lavoro che può fare solo un tecnico? y/n")
            step = 5
        elif step == 5:
            if msg['text'] == "y":
                isTecnico = 1
                bot.sendMessage(chat_id,"Ok, aggiungo al database...")
                info = (sintomo,soluzione,stepDB,isTecnico)
                bot.sendMessage(chat_id,addSolutions(db,info))
                step = 1
            else:
                isTecnico = 1
                bot.sendMessage(chat_id,"Ok, aggiungo al database...")
                info = (sintomo,soluzione,stepDB,isTecnico)
                bot.sendMessage(chat_id,addSolutions(db,info))
                step = 1
                sintomo = ""
                soluzione = ""
                stepDB = 0
                isTecnico = False

db = mysql.connector.connect(host="localhost", user="root", password="", database="drbot")

TOKEN = '1414329712:AAHUIof6BrcAWIBz7hgZqz_-tmXBb_lyPwI'
bot = telepot.Bot(TOKEN)

bot.message_loop(handle)

print("Listening...")

while 1:
    time.sleep(10)