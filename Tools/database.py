from PyQt5 import QtSql
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings, QDir


def createconnection():
    settings = QSettings()

    BDD = settings.value("BDD", defaultValue='')

    if BDD == '':
        QMessageBox.critical(None, "Base de données inconnue", "Veuillez configurer la base de données et relancer l'application")

    db = QtSql.QSqlDatabase.addDatabase('QODBC')
    db.setHostName("localhost")
    db.setDatabaseName('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};FIL={MS Access};DBQ=' + BDD)

    if db.open():
        return db
    else:
        error = db.lastError().text()
        QMessageBox.critical(None, "Database error", "Connection failed : " + error)
        return False
