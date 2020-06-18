from PyQt5 import QtSql
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMessageBox
from Tools.message import detailed_message


def createconnection():
    settings = QSettings()
    fileBDD = settings.value("BDD", defaultValue='')

    if fileBDD == '':
        QMessageBox.critical(None, "Base Access inconnue", "Veuillez configurer la base Access et relancer l'application")

    db = QtSql.QSqlDatabase.addDatabase('QODBC')
    db.setHostName("localhost")
    db.setDatabaseName('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};FIL={MS Access};DBQ=' + fileBDD)

    if db.open():
        return db
    else:
        error = db.lastError().text()
        detailed_message(None, QMessageBox.Critical, "Erreur de la base Access", "Échec de la connexion", error)
        return False
