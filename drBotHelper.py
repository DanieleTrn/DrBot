import telepot
import time
import mysql.connector
from dbManager import *

isHelping = False
step = 1
sintomo = ""
soluzione = ""
stepDB = 0
isTecnico = False

def handle(msg):
    global isHelping
    global step
    global sintomo
    global soluzione
    global stepDB
    global isTecnico

    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == "text":

        if msg['text'] == "/aggiungi" and isHelping == False:
            isHelping = True
            if step == 1 and isHelping == True:
                bot.sendMessage(chat_id,"Inserisci il sintomo")
                step = 2
        elif step == 2 and isHelping == True:
            sintomo = msg['text']
            bot.sendMessage(chat_id,"Inserisci la soluzione")
            step = 3
        elif step == 3 and isHelping == True:
            soluzione = msg['text']
            bot.sendMessage(chat_id,"Inserisci lo step")
            step = 4
        elif step == 4 and isHelping == True:
            stepDB = msg['text']
            bot.sendMessage(chat_id,"E' un lavoro che può fare solo un tecnico? y/n")
            step = 5
        elif step == 5 and isHelping == True:
            if msg['text'] == "y":
                isTecnico = 1
                bot.sendMessage(chat_id,"Ok, aggiungo al database...")
                info = (sintomo,soluzione,stepDB,isTecnico)
                bot.sendMessage(chat_id,addSolutions(db,info))
                step = 1
                sintomo = ""
                soluzione = ""
                stepDB = 0
                isTecnico = False
                isHelping = False
            else:
                isTecnico = 0
                bot.sendMessage(chat_id,"Ok, aggiungo al database...")
                info = (sintomo,soluzione,stepDB,isTecnico)
                bot.sendMessage(chat_id,addSolutions(db,info))
                step = 1
                sintomo = ""
                soluzione = ""
                stepDB = 0
                isTecnico = False
                isHelping = False

        elif msg['text'] == "/rimuovi" and isHelping == False:
            #roba
            print("ciao")


db = mysql.connector.connect(host="localhost", user="root", password="", database="drbot")

TOKEN = '1485665656:AAEGMVBohdSJpQRW6MeN_kXkNBlYdxa8r20'
bot = telepot.Bot(TOKEN)

bot.message_loop(handle)

print("Listening...")

while 1:
    time.sleep(100)