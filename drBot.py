import telepot
import time
import mysql.connector
from dbManager import *
#from botCommands import *

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == "text":
        step = 1
        
        if msg['text'] == "aggiungi" or msg['text'] == "Aggiungi":
            sintomo = ""
            soluzione = ""
            stepDB = 0
            isTecnico = False

            if step == 1:
                bot.sendMessage(chat_id,"Inserisci il sintomo")
                step = 2
            if step == 2:
                sintomo = msg['text']
                bot.sendMessage(chat_id,"Inserisci la soluzione")
                step = 3
            if step == 3:
                soluzione = msg['text']
                bot.sendMessage(chat_id,"Inserisci lo step")
                step = 4
            if step == 4:
                stepDB = msg['text']
                bot.sendMessage(chat_id,"E' un lavoro che può fare solo un tecnico? y/n")
                step = 5
            if step == 5:
                if msg['text'] == "y":
                    isTecnico = 1
                    bot.sendMessage(chat_id,"Ok, aggiungo al database...")
                    info = (sintomo,soluzione,stepDB,isTecnico)
                    bot.sendMessage(chat_id,addSolutions(db,info))
                    step = 0
                else:
                    isTecnico = 1
                    bot.sendMessage(chat_id,"Ok, aggiungo al database...")
                    info = (sintomo,soluzione,stepDB,isTecnico)
                    bot.sendMessage(chat_id,addSolutions(db,info))
                    step = 0

db = mysql.connector.connect(host="localhost", user="root", password="", database="drbot")

TOKEN = '1414329712:AAHUIof6BrcAWIBz7hgZqz_-tmXBb_lyPwI'
bot = telepot.Bot(TOKEN)

bot.message_loop(handle)

print("Listening...")

while 1:
    time.sleep(10)