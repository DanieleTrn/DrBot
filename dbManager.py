import mysql.connector

def getLastId(db): #Return last record in db
    myCursor = db.cursor()

    myCursor.execute("SELECT MAX(id_problema) from problemi")

    res = myCursor.fetchall()
    index = int(res[0][0])

    return index

def searchSolutions(db,problem): #Where "db" stands for database; "problem" a string which describe something to solve
    myCursor = db.cursor()

    problemFormat = "'"+problem+"'"

    myCursor.execute(f"SELECT * FROM problemi WHERE sintomo= {problemFormat}")

    res = myCursor.fetchall()

    return res

def lookForSteps(db,step,sintomo): #Return true if a step already exist in a symptom

    myCursor = db.cursor()

    formatText = "'" + sintomo + "'"

    myCursor.execute(f"SELECT sintomo,step FROM problemi WHERE problemi.sintomo = {formatText};")
    res = myCursor.fetchall()
    print(res)
    
    for x in res:
        if x[1] == step:
            return False #An equal step has been found

    return True #Every step is different from the one we have given
    

def addSolutions(db,solution): #Where db stands for database, solution a record to insert into it

    myCursor = db.cursor()

    idProblema = getLastId(db) + 1
    sintomo = solution[0]
    soluzione = solution[1]
    step = solution[2]
    isTecnico = solution[3]
    isDomanda = 0
    
    if lookForSteps(db,solution[2],solution[0]) == True:
        changeLaterSteps(db,solution[2])

    myCursor.execute(f"INSERT INTO problemi(id_problema,sintomo,soluzione,step,isTecnico,isDomanda) VALUES ({idProblema},'{sintomo}','{soluzione}',{step},{isTecnico},{isDomanda})")

    db.commit()

    return "Contenuto aggiunto con successo!"

def changeLaterSteps(db,newStep): #Increase by one value every record with column step greater (or equal) than the attribute "newStep"

    myCursor = db.cursor()

    res = myCursor.execute(f"UPDATE problemi SET step = (step+1) WHERE problemi.step >= {newStep};")

    db.commit()

def removeSolution(db,idSolution):

    myCursor = db.cursor()

    myCursor.execute(f"DELETE FROM problemi WHERE problemi.id_problema = {idSolution}")

    db.commit()

    return f"Eliminata soluzione n.{idSolution}"