import mysql.connector

def getOs(db):
    myCursor = db.cursor()

    myCursor.execute("SELECT distinct id_os from os")

    res = myCursor.fetchall()

    res = formatArray(res)

    return res

def getDevices(db):
    myCursor = db.cursor()

    myCursor.callproc("getDevices")
    
    for x in myCursor.stored_results():
        res = x.fetchall()

    res = formatArray(res)

    return res

def getDeviceId(db,datas): 
    myCursor = db.cursor()
    myCursor.execute(f"SELECT * FROM dispositivo WHERE dispositivo='{datas[0]}' and id_os='{datas[1]}'")

    res = myCursor.fetchall()
    
    if len(res) == 0:
        return -1

    res = res[0][0]

    return res


def getSymptoms(db,deviceType):

    myCursor = db.cursor()

    myCursor.execute(f"SELECT distinct id_sintomo from sintomo where id_dispositivo = {deviceType}")

    res = myCursor.fetchall()

    res = formatArray(res)

    return res

def formatArray(res):

    for i in range(0,len(res)):
        value = res[i][0]
        res[i] = value

    return res

def getSolutions(db, idDevice, idSymptom):
    myCursor = db.cursor()

    myCursor.execute(f"SELECT * FROM soluzione WHERE id_dispositivo = {idDevice} and id_sintomo = '{idSymptom}' order by step asc;")

    res = myCursor.fetchall()

    if len(res) == 0:
        return -1
        
    return res
    
def lookForSteps(db,step,symptom): #Return true if a step already exist in a symptom

    myCursor = db.cursor()

    myCursor.execute(f"SELECT sintomo,step FROM problemi WHERE problemi.sintomo = '{symptom}';")
    res = myCursor.fetchall()
    
    for x in res:
        if x[1] == step:
            return False #An equal step has been found

    return True #Every step is different from the ones we've given

def changeLaterSteps(db,newStep): #For every record with a column step greater or equal to the attribute NewStep, increase the value by one

    myCursor = db.cursor()

    myCursor.execute(f"UPDATE soluzione SET step = (step+1) WHERE soluzione.step >= {newStep};")

    db.commit()
