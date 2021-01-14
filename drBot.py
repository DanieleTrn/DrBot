import telepot
import time
import mysql.connector
from dbManager import *
from utils import *
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop

datas = []
step = 1
stepPrec = 1
isHelping = False
solutions = []
nSolution = 0
lenRes = 0
isTakingInfo = True
skip = {}

def handle(msg):

    global step
    global stepPrec
    global isHelping
    global nSolution
    global datas
    global isTakingInfo
    global skip
    global solutions
    global lenRes

    content_type, chat_type, chat_id = telepot.glance(msg)
    skip = getSkipMsg(msg)
    
    keyboardDevices = getKeyboard(getDevices(db)) #inlineKeyboard with button taken by database's devices
    if content_type == "text":

        if msg["text"] == "/start" and isHelping == False:
            bot.sendMessage(chat_id,"Ehi, DrBot al tuo servizio! Mi serviranno un pò di info riguardo il paziente, tranquillo, saranno poche domande")
            isHelping = True
            time.sleep(3)

            bot.sendMessage(chat_id,"Quale dispositivo ti sta dando problemi?", reply_markup=keyboardDevices)
            isTakingInfo = True
            
        elif(len(datas) == 1) and isHelping and msg["text"] != "/stop" and isTakingInfo == False:

            osKeyboard = getKeyboard(getOs(db))
            bot.sendMessage(chat_id,f"Perfetto, Dispositivo: {datas[0]}")
            time.sleep(2)

            bot.sendMessage(chat_id,"Qual è il suo sistema operativo?",reply_markup=osKeyboard)
            isTakingInfo = True

        elif(len(datas) == 2) and isHelping and msg["text"] != "/stop" and isTakingInfo == False:

            deviceId = getDeviceId(db,datas)
            if deviceId != -1:

                symptomsKeyboard = getKeyboard(getSymptoms(db,deviceId))
                bot.sendMessage(chat_id,"Perfetto perfetto, ho già avuto a che fare con certi dispositivi!")
                time.sleep(2)

                bot.sendMessage(chat_id,"Dimmi, di cosa soffre il paziente?", reply_markup=symptomsKeyboard)
                isTakingInfo = True
            else:

                bot.sendMessage(chat_id,"Oh...non ho mai avuto a che fare con un paziente simile! Avverto il capo e ti faccio contattare da lui il prima possibile.")
                #bot.sendMessage(davide_id,msg) qui avvertirò davide

        elif(len(datas) == 3) and isHelping and msg["text"] != "/stop" and isTakingInfo == False:
            if(step == 1):

                bot.sendMessage(chat_id,"Bene, ho tutto quello che mi serve...vediamo...")
                deviceId = getDeviceId(db,datas)
                solutions = getSolutions(db,deviceId,datas[2])
                lenRes = len(solutions)

                time.sleep(2)

                bot.sendMessage(chat_id,"Ho raccolto delle soluzioni che potrebbero aiutarci, se non funzioneranno contatterò il capo. Iniziamo!")
                step += 1

                time.sleep(2)

                handle(skip)

            elif(step == stepPrec + 1 and isHelping == True):

                bot.sendMessage(chat_id,solutions[nSolution][3])
                time.sleep(2)
                bot.sendMessage(chat_id,"Hai risolto? scrivi si o no")
                stepPrec += 1

            elif (step == stepPrec and isHelping == True):

                formatMsg = msg['text'].lower()

                if(formatMsg == "si" or formatMsg == "yes" or formatMsg == "y"):

                    bot.sendMessage(chat_id,"Felice di aver aiutato, alla prossima!")
                    step = 1
                    stepPrec = 1
                    isHelping = False
                    nSolution = 0
                    solutions = []
                    datas = []

                elif(formatMsg == "no" or formatMsg == "n"):
                    nSolution += 1
                    if nSolution >= lenRes:
                        bot.sendMessage(chat_id,"Non ho idea di cosa possa essere, provo a contattare il capo!")
                        step = 1
                        stepPrec = 1
                        isHelping = False
                        nSolution = 0
                        solutions = []
                        datas = []
                    else:
                        bot.sendMessage(chat_id,"Proviamo qualcos'altro")
                        step += 1
                        handle(skip)

        elif msg["text"] == "/stop":
            if isHelping:
                bot.sendMessage(chat_id, "Ok, interrompiamo tutto!")
                datas = []
                isHelping = False
                nSolution = 0
                step = 1
                stepPrec = 1
                solutions = []
            else:
                bot.sendMessage(chat_id,"Si? Che c'è?")



def on_callback_query(msg):

    global isTakingInfo
    print(datas)
    print(isHelping)
    print(solutions)
    print(nSolution)

    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")

    if(isTakingInfo == True):
        datas.append(query_data)
        isTakingInfo = False
        handle(skip)

#Put your db's info where value is "xxx"
db = mysql.connector.connect(host="xxx", user="xxx", password="", database="xxx")

TOKEN = 'xxx' #Put your bot's token here

bot = telepot.Bot(TOKEN)

MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()

print("Listening...")

while 1:
    time.sleep(100)