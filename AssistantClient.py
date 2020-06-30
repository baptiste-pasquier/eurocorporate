import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5 import QtCore, QtSql, QtWidgets, uic
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import (QDialogButtonBox, QFileDialog, QMessageBox,
                             QProgressDialog)
                             ###

# qt_creator_file = "portefeuille.ui"
# Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)
import AssistantClientUI
from AssistantClientUI import Ui_MainWindowClient


def createconnection():
    db = QtSql.QSqlDatabase.addDatabase('QODBC')
    db.setHostName("localhost")
    db.setDatabaseName('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};FIL={MS Access};DBQ=C:\\Users\\Aquaquaq\\OneDrive\\Bureau\\Cours\\pro\\ROCKLEE\\IS_beC.mdb')


    if db.open():
        print('connect to SQL Server successfully')
        return db
    else:
        print('connection failed')
        print(db.lastError().text())
        return False

class ModelClient(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Client')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()


    def data(self, index, role=Qt.DisplayRole):

            # Affichage noClient
            noClient_column = self.fieldIndex('noClient')
            nomEntreprise_column = self.fieldIndex('nomEntreprise')
            if role == Qt.DisplayRole and index.column() == noClient_column:
                noClient = super().data(index, 0)
                nomEntreprise = super().data(self.index(index.row(), nomEntreprise_column), 0)
                value = '{'+'{:0>2d}}} {}'.format(noClient, nomEntreprise)
                return value
            return super().data(index, role)



class MainWindowClient(QtWidgets.QMainWindow, Ui_MainWindowClient):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindowClient.__init__(self)
        self.setupUi(self)

        self.db = createconnection()

        self.modelClient = ModelClient()
        self.modelClient.select()

        self.pushButton_Valider.clicked.connect(self.new_client)

# Liste des clients
        self.modelClient = ModelClient()
        #self.clientChoisi = Client()

        self.fontComboBox_ModClient.setModel(self.modelClient)
        self.fontComboBox_ModClient.setModelColumn(self.modelClient.fieldIndex('nomEntreprise'))
        self.fontComboBox_ModClient.setCurrentIndex(-1)

        self.pushButton_ModValider.clicked.connect(self.mod_client)

        self.fontComboBox_SupprClient.setModel(self.modelClient)
        self.fontComboBox_SupprClient.setModelColumn(self.modelClient.fieldIndex('nomEntreprise'))
        self.fontComboBox_SupprClient.setCurrentIndex(-1)
        self.pushButton_SupprValider.clicked.connect(self.suppr_client)
    def new_client(self):

        nom_entreprise = self.lineEdit_Entreprise.text()
        nom_contact =self.lineEdit_ContactName.text()
        prenom_contact =self.lineEdit_ContactForename.text()
        mail_contact = self.lineEdit_Mail.text()

        if nom_entreprise != '':
            model = self.modelClient
            new_row = model.record()

            # Nouveau numéro du Client
            query = QtSql.QSqlQuery()
            query.exec("SELECT MAX(noClient) FROM Client")
            if query.next():
                max_no_client = int(query.value(0))
            query.finish()

            defaults = {
                'noClient': max_no_client + 1,
                'nomEntreprise' : nom_entreprise,
                'nomContact' : nom_contact,
                'prenomContact' : prenom_contact,
                'mailContact' : mail_contact
                }

            for field, value in defaults.items():
                index = model.fieldIndex(field)
                new_row .setValue(index, value)

            inserted = model.insertRecord(-1, new_row)
            if not inserted:
                error = model.lastError().text()
                print(f"Insert Failed: {error}")
                model.select()

            if model.submitAll():
                QMessageBox.information(self, "Nouveau Client", "Ajout réussi")
            else:
                error = model.lastError().text()
                QMessageBox.critical(self, "Database returned an error", error)
        else:
            error = model.lastError().text()
            QMessageBox.critical(self, "Oubli du nom de l'entreprise'", error)

    def mod_client(self):
        model = self.modelClient
        #le client et ses mod. sont récupérés dans les ligne éditables
        client_choisi = "'" + self.fontComboBox_ModClient.currentText() + "'"

        nom_entreprise = self.lineEdit_ModEntreprise.text()
        nom_contact = self.lineEdit_ModContactName.text()
        prenom_contact = self.lineEdit_ModContactForename.text()
        mail_contact = self.lineEdit_ModMail.text()

        old_nom_entreprise = ""
        old_nom_contact = ""
        old_prenom_contact = ""
        old_mail_contact = ""
        query = QtSql.QSqlQuery()
        query.exec("SELECT noClient, nomEntreprise, nomContact,prenomContact, mailContact FROM Client WHERE nomEntreprise =" + client_choisi)
        if query.next():
            no_client = int(query.value(0))
            if type(query.value(1)) == str:
                old_nom_entreprise = query.value(1)
            else:
                old_nom_entreprise = ""
            if type(query.value(2)) == str:
                old_nom_contact = query.value(2)
            else:
                old_nom_contact = ""
            if type(query.value(3)) == str:
                old_prenom_contact = query.value(3)
            else:
                old_prenom_contact = ""
            if type(query.value(4)) == str:
                old_mail_contact = query.value(4)
            else:
                old_mail_contact = ""
        else:
            error = model.lastError().text()
            print("erreur")
            QMessageBox.critical(self, "erreur 1", error)
        query.clear()
        modEntreprise = str(nom_entreprise *(nom_entreprise != '') + old_nom_entreprise * (nom_entreprise == '' ) )
        modNom = str (nom_contact *(nom_contact != '') + old_nom_contact * (nom_contact == '') )
        modPrenom = str(prenom_contact *(prenom_contact != '') + old_prenom_contact * (prenom_contact == '') )
        modMail = str (mail_contact *(mail_contact != '') + old_mail_contact * (mail_contact == '') )


        query2 = QtSql.QSqlQuery()
        result = query2.exec("UPDATE Client SET nomEntreprise = '" + modEntreprise +"', nomContact = '" + modNom +"', prenomContact = '"+ modPrenom +"', mailContact = '"+ modMail +"' WHERE noClient = " + str(no_client) )

        if result:
            QMessageBox.information(self, "Client Modifié", "Modification Reussie")
            self.lineEdit_Entreprise.clear()
            self.lineEdit_ContactName.clear()
            self.lineEdit_ContactForename.clear()
            self.lineEdit_Mail.clear()

        else:
            error = model.lastError().text()
            QMessageBox.critical(self, "Database returned an error", error)

    def suppr_client(self):
        model = self.modelClient
        client_choisi = "'" + self.fontComboBox_SupprClient.currentText() + "'"

        query = QtSql.QSqlQuery()
        result = query.exec("DELETE FROM Client WHERE nomEntreprise = " + client_choisi )
        if result:
            QMessageBox.information(self, "Client Supprimé", "Modification Reussie")
        else:
            error = model.lastError().text()
            QMessageBox.critical(self, "Database returned an error", error)

app = QtWidgets.QApplication(sys.argv)
window = MainWindowClient()
window.show()
app.exec_()
window.show
###
#la création de client marche !!!