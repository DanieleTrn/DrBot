import mysql.connector

def getLastId(db): #return last record in db
    myCursor = db.cursor()

    myCursor.execute("SELECT MAX(id_problema) from problemi")

    res = myCursor.fetchall()
    index = int(res[0][0])

    return index

def searchSolutions(db,problem): #where "db" stands for database; "problem" a string which describe something to solve
    myCursor = db.cursor()

    problemFormat = "'"+problem+"'"

    myCursor.execute(f"SELECT * FROM problemi WHERE sintomo= {problemFormat}")

    res = myCursor.fetchall()

    return res

def addSolutions(db,solution): #where db stands for database, solution a record to insert into it

    myCursor = db.cursor()

    idProblema = getLastId(db) + 1
    sintomo = "'"+solution[0]+"'"
    soluzione = "'"+solution[1]+"'"
    step = solution[2]
    isTecnico = solution[3]

    myCursor.execute(f"INSERT INTO problemi(id_problema,sintomo,soluzione,step,isTecnico) VALUES ({idProblema},{sintomo},{soluzione},{step},{isTecnico})")

    db.commit()

    return "Contenuto aggiunto con successo!"

def removeSolution(db,idSolution):

    myCursor = db.cursor()

    myCursor.execute(f"DELETE FROM problemi WHERE problemi.id_problema = {idSolution}")

    db.commit()

    return f"Eliminata soluzione n.{idSolution}"