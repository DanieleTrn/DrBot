import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="", database="drbot")

myCursor = db.cursor()

myCursor.callproc("GetDevices")
for result in myCursor.stored_results():
    res = (result.fetchall())

print(res)
