import mysql.connector
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from dbManager import *

def getKeyboard(items): # InlineKeyboard con bottoni ottenuti dai record contenuti in items
        buttons = []
        for i in range(0,len(items)):
            button = [InlineKeyboardButton(text=f"{items[i]}", callback_data = f"{items[i]}")]
            buttons.append(button)

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

def getSkipMsg(msg): #Ritorna un dizionario utilizzato per automatizzare alcuni dialoghi
    skip = msg
    skip['chat']['text'] = "a"
    skip['chat']['reply_markup'] = None

    return skip