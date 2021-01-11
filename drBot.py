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
res = []
nSolution = 0
lenRes = 0
isTakingInfo = True
skip = {}

def handle(msg):

    global step
    global stepPrec
    global isHelping
    global res
    global nSolution
    global lenRes
    global datas
    global isTakingInfo
    global skip
    
    content_type, chat_type, chat_id = telepot.glance(msg)
    skip = getSkipMsg(msg)
    #keyboard = InlineKeyboardMarkup(inline_keyboard= [
               #[InlineKeyboardButton(text="Cliccami",callback_data="press")],
                #])
    
    keyboardDevices = getKeyboard(getDevices(db)) #inlineKeyboard with button taken by database's devices
    if content_type == "text":

        if msg["text"] == "/start" and isHelping == False:
            bot.sendMessage(chat_id,"Ehi, DrBot al tuo servizio! Mi serviranno un pò di info riguardo il paziente, tranquillo, saranno poche domande")
            isHelping = True
            time.sleep(3)

            bot.sendMessage(chat_id,"Quale dispositivo ti sta dando problemi?", reply_markup=keyboardDevices)
        elif(len(datas) == 1) and isHelping and msg["text"] != "/stop":

            osKeyboard = getKeyboard(getOs(db))
            bot.sendMessage(chat_id,f"Perfetto, Dispositivo: {datas[0]}")
            time.sleep(2)

            bot.sendMessage(chat_id,"Qual è il suo sistema operativo?",reply_markup=osKeyboard)
            isTakingInfo = True

        elif(len(datas) == 2) and isHelping and msg["text"] != "/stop":

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

        elif(len(datas) == 3) and isHelping and msg["text"] != "/stop":

            bot.sendMessage(chat_id,"Bene, ho tutto quello che mi serve...vediamo...")
            deviceId = getDeviceId(db,datas)
            solutions = getSolutions(db,deviceId,datas[2])
            time.sleep(2)
            print(solutions)
            bot.sendMessage(chat_id,"Ho raccolto delle soluzioni che potrebbero aiutarci, se non funzioneranno contatterò il capo. Iniziamo!")
            step += 1
        elif msg["text"] == "ehi":
            print(datas)
        
        elif msg["text"] == "/stop":
            if isHelping:
                bot.sendMessage(chat_id, "Ok, interrompiamo tutto!")
                datas = []
                isHelping = False
            else:
                bot.sendMessage(chat_id,"Si? Che c'è?")



def on_callback_query(msg):

    global isTakingInfo

    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")

    if(isTakingInfo == True):
        datas.append(query_data)
        isTakingInfo = False
        handle(skip)


db = mysql.connector.connect(host="localhost", user="root", password="", database="drbot")

TOKEN = '1414329712:AAHUIof6BrcAWIBz7hgZqz_-tmXBb_lyPwI'
bot = telepot.Bot(TOKEN)

#bot.message_loop({"chat": handle, "callback_query": on_callback_query}).run_as_thread()
#MessageLoop(bot).run_as_thread()
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print("Listening...")

while 1:
    time.sleep(100)