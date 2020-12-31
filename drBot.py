import telepot
import time
import mysql.connector
from dbManager import *

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
        
        ##TEST###
        if msg['text'] == "start":
            bot.sendMessage(chat_id,"Ehi,dimmi il tuo problema!")
            nSolution = 0
            res = searchSolutions(db,"pc spento")
            lenRes = len(res)
            step += 1
            isHelping = True
        elif step == stepPrec + 1 and isHelping == True:
                bot.sendMessage(chat_id,res[nSolution][2])
                bot.sendMessage(chat_id,"Hai risolto?")
                stepPrec += 1
        elif step == stepPrec and isHelping == True:
                formatMsg = msg['text'].lower()
                if(formatMsg == "si" or formatMsg == "yes" or formatMsg == "y"):
                    bot.sendMessage(chat_id,"So felice per te")
                    step = 1
                    stepPrec = 1
                    isHelping = False
                    nSolution = 0
                    res = []
                elif(formatMsg == "no" or formatMsg == "n"):
                    nSolution += 1
                    if nSolution >= lenRes:
                        bot.sendMessage(chat_id,"Non ho idea di cosa possa essere, provo a contattare il boss!")
                        isHelping = False
                        step = 1
                        stepPrec = 1
                        isHelping = False
                        nSolution = 0
                        res = []
                    else:
                        bot.sendMessage(chat_id,"Proviamo qualcos'altro, scrivi qualsiasi cosa quando sei pronto...")
                        step += 1

db = mysql.connector.connect(host="localhost", user="root", password="", database="drbot")

TOKEN = '1414329712:AAHUIof6BrcAWIBz7hgZqz_-tmXBb_lyPwI'
bot = telepot.Bot(TOKEN)

bot.message_loop(handle)

print("Listening...")

while 1:
    time.sleep(100)