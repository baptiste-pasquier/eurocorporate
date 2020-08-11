from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from Assistants.AssistantClientUI import Ui_MainWindowClient


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


class MainWindowClient(QtWidgets.QMainWindow, Ui_MainWindowClient):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        Ui_MainWindowClient.__init__(self)
        self.setupUi(self)

        self.modelClient = ModelClient()
        self.modelClient.select()

        self.pushButton_Valider.clicked.connect(self.new_client)

        # Liste des clients
        self.modelClient = ModelClient()
        # self.clientChoisi = Client()

        self.comboBox_ModClient.setModel(self.modelClient)
        self.comboBox_ModClient.setModelColumn(self.modelClient.fieldIndex('nomEntreprise'))
        self.comboBox_ModClient.setCurrentIndex(-1)
        self.comboBox_ModClient.activated.connect(self.rempli_mod)

        self.pushButton_ModValider.clicked.connect(self.mod_client)

        self.comboBox_SupprClient.setModel(self.modelClient)
        self.comboBox_SupprClient.setModelColumn(self.modelClient.fieldIndex('nomEntreprise'))
        self.comboBox_SupprClient.setCurrentIndex(-1)
        self.pushButton_SupprValider.clicked.connect(self.suppr_client)

        self.cbClient_portefeuille = None   # Pour mettre à jour le modelClient dans le gestionnaire de portefeuille, si ouvert depuis le gestionnaire de portefeuille

    def new_client(self):

        nom_entreprise = self.lineEdit_Entreprise.text()
        nom_contact = self.lineEdit_ContactName.text()
        prenom_contact = self.lineEdit_ContactForename.text()
        mail_contact = self.lineEdit_Mail.text()
        tel_contact = int(self.lineEdit_Tel.text())
        comment = self.textEdit_Comment.text()

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
                'nomEntreprise': nom_entreprise,
                'nomContact': nom_contact,
                'prenomContact': prenom_contact,
                'mailContact': mail_contact,
                'telContact' : tel_contact,
                'commentaire' : comment
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
                self.update_cbClient_portefeuille() # Pour mettre à jour le modelClient dans le gestionnaire de portefeuille, si ouvert depuis le gestionnaire de portefeuille
                self.lineEdit_Entreprise.clear()
                self.lineEdit_ContactName.clear()
                self.lineEdit_ContactForename.clear()
                self.lineEdit_Mail.clear()
                self.lineEdit_Tel.clear()
                self.textEdit_Comment.clear()
            else:
                error = model.lastError().text()
                QMessageBox.critical(self, "Database returned an error", error)
        else:
            error = model.lastError().text()
            QMessageBox.critical(self, "Oubli du nom de l'entreprise'", error)

    def rempli_mod(self):
        model = self.modelClient
        # le client et ses mod. sont récupérés dans les ligne éditables
        client_choisi = "'" + self.comboBox_ModClient.currentText() + "'"
        query = QtSql.QSqlQuery()
        query.exec("SELECT noClient, nomEntreprise, nomContact,prenomContact, mailContact, telContact, commentaire FROM Client WHERE nomEntreprise =" + client_choisi)

        if query.next():

            nomentreprise2 = str(query.value(1))
            nomcontact2 =str(query.value(2))
            prenomcontact2 = str(query.value(3))
            mailcontact2 = str(query.value(4))
            numcontact2 = int(query.value(5))
            comment2 = str(query.value(6))

        else:
            error = model.lastError().text()
            QMessageBox.critical(self, "erreur 1", error)
        query.clear()

        self.lineEdit_ModEntreprise.setText(nomentreprise2)
        self.lineEdit_ModContactName.setText(nomcontact2)
        self.lineEdit_ModContactForename.setText(prenomcontact2)
        self.lineEdit_ModMail.setText(mailcontact2)
        self.lineEdit_ModTel.setText(numcontact2)
        self.textEdit_ModComment.setText(comment2)

    def mod_client(self):
        model = self.modelClient
        # le client et ses mod. sont récupérés dans les ligne éditables
        client_choisi = "'" + self.comboBox_ModClient.currentText() + "'"

        nom_entreprise = self.lineEdit_ModEntreprise.text()
        nom_contact = self.lineEdit_ModContactName.text()
        prenom_contact = self.lineEdit_ModContactForename.text()
        mail_contact = self.lineEdit_ModMail.text()
        tel_contact = int(self.lineEdit_ModTel.text())
        comment = self.textEdit_ModComment.text()

        old_nom_entreprise = ""
        old_nom_contact = ""
        old_prenom_contact = ""
        old_mail_contact = ""
        old_num = 0
        old_comment = ""
        query = QtSql.QSqlQuery()
        query.exec("SELECT noClient, nomEntreprise, nomContact,prenomContact, mailContact, telContact, commentaire FROM Client WHERE nomEntreprise =" + client_choisi)

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
            if type(query.value(5)) == int:
                old_num = query.value(5)
            else:
                old_num = 0
            if type(query.value(6)) ==str:
                old_comment = query.value(6)
            else:
                old_comment = ""
        else:
            error = model.lastError().text()
            QMessageBox.critical(self, "Le client n'a pas été trouvé'", error)

        query.clear()

        modEntreprise = str(nom_entreprise * (nom_entreprise != '') + old_nom_entreprise * (nom_entreprise == ''))
        modNom = str(nom_contact * (nom_contact != '') + old_nom_contact * (nom_contact == ''))
        modPrenom = str(prenom_contact * (prenom_contact != '') + old_prenom_contact * (prenom_contact == ''))
        modMail = str(mail_contact * (mail_contact != '') + old_mail_contact * (mail_contact == ''))

        modTel = tel_contact * (tel_contact != 0) + old_num * (tel_contact ==0)
        modComment = str(comment * (comment != '') + old_comment * (comment == ''))


        query2 = QtSql.QSqlQuery()
        result = query2.exec("UPDATE Client SET nomEntreprise = '" + modEntreprise + "', nomContact = '" + modNom + "', prenomContact = '" + modPrenom + "', mailContact = '" + modMail + "' , telContact = "+ modTel + ", commentaire = '" + modComment  + "' WHERE noClient = " + str(no_client))

        if result:
            QMessageBox.information(self, "Client Modifié", "Modification Reussie")
            self.lineEdit_ModEntreprise.clear()
            self.lineEdit_ModContactName.clear()
            self.lineEdit_ModContactForename.clear()
            self.lineEdit_ModMail.clear()
            self.lineEdit_ModTel.clear()
            self.textEdit_ModComment.clear()

            self.update_cbClient_portefeuille() # Pour mettre à jour le modelClient dans le gestionnaire de portefeuille, si ouvert depuis le gestionnaire de portefeuille
        else:
            error = model.lastError().text()
            QMessageBox.critical(self, "Database returned an error", error)

    def suppr_client(self):

        model = self.modelClient
        client_choisi = "'" + self.comboBox_SupprClient.currentText() + "'"

        query = QtSql.QSqlQuery()
        result = query.exec("DELETE FROM Client WHERE nomEntreprise = " + client_choisi)

        if result:
            QMessageBox.information(self, "Client Supprimé", "Modification Reussie")
            self.update_cbClient_portefeuille() # Pour mettre à jour le modelClient dans le gestionnaire de portefeuille, si ouvert depuis le gestionnaire de portefeuille
        else:
            error = model.lastError().text()
            QMessageBox.critical(self, "Database returned an error", error)

    def set_cbClient_portefeuille(self, cb):
        # Pour mettre à jour le modelClient dans le gestionnaire de portefeuille, si ouvert depuis le gestionnaire de portefeuille
        self.cbClient_portefeuille = cb

    def update_cbClient_portefeuille(self):
        # Pour mettre à jour le modelClient dans le gestionnaire de portefeuille, si ouvert depuis le gestionnaire de portefeuille
        if self.cbClient_portefeuille:
            self.cbClient_portefeuille.model().select()
            self.cbClient_portefeuille.setCurrentIndex(-1)
