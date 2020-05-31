from PyQt5 import QtSql

def createconnection():
    db = QtSql.QSqlDatabase.addDatabase('QODBC')
    db.setHostName("localhost")
    db.setDatabaseName('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};FIL={MS Access};DBQ=C:\\Users\\pasqu\\OneDrive\\Documents\\Scolaire\\ENSAE\\Mission JE\\CodeBaptiste\\IS_beC.mdb')


    if db.open():
        print('connect to SQL Server successfully')
        return db
    else:
        print('connection failed')
        print(db.lastError().text())
        return False