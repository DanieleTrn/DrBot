import mysql.connector
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def getKeyboard(items):
        buttons = []
        for i in range(0,len(items)):
            button = [InlineKeyboardButton(text=f"{items[i]}", callback_data = f"{items[i]}")]
            buttons.append(button)

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
        