from PyQt5 import QtSql
from PyQt5.QtWidgets import QMessageBox


def createconnection():
    db = QtSql.QSqlDatabase.addDatabase('QODBC')
    db.setHostName("localhost")
    db.setDatabaseName('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};FIL={MS Access};DBQ=C:\\Users\\pasqu\\OneDrive\\Documents\\Scolaire\\ENSAE\\Mission JE\\CodeBaptiste\\IS_beC.mdb')

    if db.open():
        return db
    else:
        error = db.lastError().text()
        QMessageBox.critical(None, "Database error", "Connection failed : " + error)
        return False
