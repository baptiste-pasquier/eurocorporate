from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from Assistants.FicheClientUI import Ui_WindowFicheClient


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
            value = '{' + '{:0>2d}}} {}'.format(noClient, nomEntreprise)
            return value
        return super().data(index, role)

class WindowFicheClient(QtWidgets.QMainWindow, Ui_WindowFicheClient):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        Ui_WindowFicheClient.__init__(self)
        self.setupUi(self)


        self.modelClient = ModelClient()
        self.modelClient.select()

        # Liste des clients
        self.modelClient = ModelClient()
        # self.clientChoisi = Client()

        self.comboBox_Client.setModel(self.modelClient)
        self.comboBox_Client.setModelColumn(self.modelClient.fieldIndex('nomEntreprise'))
        self.comboBox_Client.setCurrentIndex(-1)
        self.comboBox_Client.activated.connect(self.rempli)

    def rempli(self):
        # le client et ses mod. sont récupérés dans les ligne éditables
        client_choisi = "'" + self.comboBox_Client.currentText() + "'"
        query = QtSql.QSqlQuery()
        query.exec("SELECT noClient, nomEntreprise, nomContact, prenomContact, mailContact, telContact, commentaires FROM Client WHERE nomEntreprise =" + client_choisi)

        if query.first():
            nomentreprise = str(query.value(1))
            nomcontact = str(query.value(2))
            prenomcontact = str(query.value(3))
            mailcontact = str(query.value(4))
            telcontact = str(query.value(5))
            commentaires = str(query.value(6))

        self.lineEdit_Entreprise.setText(nomentreprise)
        self.lineEdit_ContactName.setText(nomcontact)
        self.lineEdit_ContactForename.setText(prenomcontact)
        self.lineEdit_Mail.setText(mailcontact)
        self.lineEdit_Tel.setText(telcontact)
        self.textEdit_Commentaires.setText(commentaires)
