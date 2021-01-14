import telepot
import time
import mysql.connector
from dbManager import *
from utils import *
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop

datas = [] #Qui andremo a collezionare le informazioni necessarie al bot

#Variabili utilizzate per iterare le varie soluzioni proposte dal bot
step = 1
stepPrec = 1

isHelping = False #Flag che indica se il nostro bot è "in servizio"
solutions = [] #Qui vengono immagazzinati i record delle soluzioni proposte

#Variabili che andremo a utilizzare per iterare le soluzioni raccolte dal bot
nSolution = 0
lenRes = 0

isTakingInfo = True #Flag utilizzata per limitare errori dovuti a click errati nelle InlineKeyboard dall'utente
skip = {} #Un dizionario che andrà ad automatizzare determinati dialoghi (vedi riga 35)

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
    skip = getSkipMsg(msg) #Variabile utilizzata per inviare messaggi falsi al bot per automatizzare dialoghi
    
    keyboardDevices = getKeyboard(getDevices(db)) #inlineKeyboard with button taken by database's devices
    if content_type == "text":

        #Da qui il bot capirà quale risposta dare all'utente in base ai dati collezionati nella variabile datas.

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

            #Da qui le informazioni sono iterate seguendo questa logica:
            #Se step è maggiore di stepPrec significa che sto mandando una soluzione, aumento stepPrec, se sono uguali
            #il bot sta aspettando una risposta dall'utente che in base ad essa capirà se inviare una ulteriore soluzione o no
            #se dovessero terminare le soluzioni, il bot invierà un messaggio al "tecnico". 
            elif(step == stepPrec + 1 and isHelping == True):

                bot.sendMessage(chat_id,solutions[nSolution][3])
                time.sleep(2)
                bot.sendMessage(chat_id,"Hai risolto? scrivi si o no")
                stepPrec += 1

            elif (step == stepPrec and isHelping == True):

                formatMsg = msg['text'].lower() #formatto la risposta in minuscolo per garantire una risposta (se pertinente)

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

        elif msg["text"] == "/stop": #Interrompe la sessione con l'utente.
            if isHelping:
                bot.sendMessage(chat_id, "Ok, interrompiamo tutto!")

                #Pulisco ogni variabile.
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

    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")

    if(isTakingInfo == True):
        datas.append(query_data) #colleziono l'informazione di cui ho bisogno
        isTakingInfo = False #Il pulsante è stato selezionato, questa variabile rimarrà falsa finchè non si presenterà una nuova tastiera
        handle(skip) #Il pulsante è stato selezionato, invio un messaggio per provocare una risposta automatica dal bot

#Put your db's info where value is "xxx"
db = mysql.connector.connect(host="xxx", user="xxx", password="", database="xxx")

TOKEN = 'xxx' #Put your bot's token here

bot = telepot.Bot(TOKEN)

MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()

print("Listening...")

while 1:
    time.sleep(100)