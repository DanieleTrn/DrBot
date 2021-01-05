import mysql.connector

#Methods:
#getLastId() TODO
#getDevices(database db) it returns every devices on our db
#getSymptoms(database db, int devicetype) 
#getSolutions()TODO
#lookForSteps(database db, int step, String sintomo)
#addSolution() TODO
#changeLaterSteps(database db, int newStep)
#removeSolution() TODO
#formatArray(array[] res)

###############################################################################
def getLastId(db): #Return last record in db
    print("Ciao")
    #TODO
###############################################################################

def getDevices(db):
    myCursor = db.cursor()

    myCursor.callproc("getDevices")
    
    for x in myCursor.stored_results():
        res = x.fetchall()

    res = formatArray(res)

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

    return res
    
def lookForSteps(db,step,symptom): #Return true if a step already exist in a symptom

    myCursor = db.cursor()

    myCursor.execute(f"SELECT sintomo,step FROM problemi WHERE problemi.sintomo = '{symptom}';")
    res = myCursor.fetchall()
    
    for x in res:
        if x[1] == step:
            return False #An equal step has been found

    return True #Every step is different from the ones we've given

###################################################################################
def addSolutions(db): #Where db stands for database
    print("Ciao")
    #TODO
##################################################################################

def changeLaterSteps(db,newStep): #For every record with a column step greater or equal to the attribute NewStep, increase the value by one

    myCursor = db.cursor()

    res = myCursor.execute(f"UPDATE soluzione SET step = (step+1) WHERE soluzione.step >= {newStep};")

    db.commit()

#################################################################################
def removeSolution():
    print("Ciao")
    #TODO
#################################################################################