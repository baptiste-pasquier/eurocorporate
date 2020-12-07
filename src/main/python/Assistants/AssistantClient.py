from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from Assistants.AssistantClientUI import Ui_MainWindowClient
from Tools.message import detailed_message


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
        tel_contact = self.lineEdit_Tel.text()
        comment = self.textEdit_Comment.toPlainText()

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
                'commentaires' : comment
                }

            for field, value in defaults.items():
                index = model.fieldIndex(field)
                new_row .setValue(index, value)

            inserted = model.insertRecord(-1, new_row)
            if not inserted:
                error = model.lastError().text()
                # ERROR
                detailed_message(self, QMessageBox.Critical, "Erreur Python", "Échec de l'insertion du client", error)

            if model.submitAll():
                QMessageBox.information(self, "Nouveau Client", "Ajout réussi")
                model.select()
                self.comboBox_ModClient.setCurrentIndex(-1)
                self.comboBox_SupprClient.setCurrentIndex(-1)
                self.lineEdit_ModEntreprise.clear()
                self.lineEdit_ModContactName.clear()
                self.lineEdit_ModContactForename.clear()
                self.lineEdit_ModMail.clear()
                self.lineEdit_ModTel.clear()
                self.textEdit_ModComment.clear()
                self.update_cbClient_portefeuille()  # Pour mettre à jour le modelClient dans le gestionnaire de portefeuille, si ouvert depuis le gestionnaire de portefeuille
                self.lineEdit_Entreprise.clear()
                self.lineEdit_ContactName.clear()
                self.lineEdit_ContactForename.clear()
                self.lineEdit_Mail.clear()
                self.lineEdit_Tel.clear()
                self.textEdit_Comment.clear()
            else:
                error = model.lastError().text()
                # ERROR
                detailed_message(self, QMessageBox.Critical, "Erreur de la base Access", "Échec de l'insertion du client", error)

        else:
            QMessageBox.critical(self, "Ajout impossible", "Merci de spécifier un nom d'entreprise")

    def rempli_mod(self):
        # le client et ses mod. sont récupérés dans les ligne éditables
        client_choisi = "'" + self.comboBox_ModClient.currentText() + "'"
        query = QtSql.QSqlQuery()
        query.exec("SELECT noClient, nomEntreprise, nomContact,prenomContact, mailContact, telContact, commentaires FROM Client WHERE nomEntreprise =" + client_choisi)

        if query.next():

            nomentreprise2 = str(query.value(1))
            nomcontact2 = str(query.value(2))
            prenomcontact2 = str(query.value(3))
            mailcontact2 = str(query.value(4))
            numcontact2 = str(query.value(5))
            comment2 = str(query.value(6))

        else:
            error = query.lastError().text()
            # ERROR
            detailed_message(self, QMessageBox.Critical, "Erreur de la base Access", "Lecture impossible", error)

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
        tel_contact = self.lineEdit_ModTel.text()
        comment = self.textEdit_ModComment.toPlainText()

        query = QtSql.QSqlQuery()
        query.exec("SELECT noClient, nomEntreprise, nomContact,prenomContact, mailContact, telContact, commentaires FROM Client WHERE nomEntreprise =" + client_choisi)

        if query.next():
            no_client = int(query.value(0))
        else:
            error = query.lastError().text()
            # ERROR
            detailed_message(self, QMessageBox.Critical, "Erreur de la base Access", "Client non trouvé", error)

        query.clear()

        modEntreprise = str(nom_entreprise)
        modNom = str(nom_contact)
        modPrenom = str(prenom_contact)
        modMail = str(mail_contact)
        modTel = str(tel_contact)
        modComment = str(comment)

        query2 = QtSql.QSqlQuery()
        chaine = "UPDATE Client SET nomEntreprise = '" + modEntreprise + "', nomContact = '" + modNom + "', prenomContact = '" + modPrenom + "', mailContact = '" + modMail + "', telContact = '" + modTel + "', commentaires = '" + modComment + "' WHERE noClient = " + str(no_client)
        result = query2.exec(chaine)

        if result:
            QMessageBox.information(self, "Client Modifié", "Modification réussie")
            self.update_cbClient_portefeuille()  # Pour mettre à jour le modelClient dans le gestionnaire de portefeuille, si ouvert depuis le gestionnaire de portefeuille
        else:
            error = query2.lastError().text()
            # ERROR
            detailed_message(self, QMessageBox.Critical, "Erreur de la base Access", "Échec de la modification du client", error)

    def suppr_client(self):
        model = self.modelClient
        client_choisi = "'" + self.comboBox_SupprClient.currentText() + "'"

        query = QtSql.QSqlQuery()
        result = query.exec("DELETE FROM Client WHERE nomEntreprise = " + client_choisi)

        if result:
            QMessageBox.information(self, "Client Supprimé", "Modification réussie")
            model.select()
            self.comboBox_ModClient.setCurrentIndex(-1)
            self.comboBox_SupprClient.setCurrentIndex(-1)
            self.lineEdit_ModEntreprise.clear()
            self.lineEdit_ModContactName.clear()
            self.lineEdit_ModContactForename.clear()
            self.lineEdit_ModMail.clear()
            self.lineEdit_ModTel.clear()
            self.textEdit_ModComment.clear()
            self.update_cbClient_portefeuille()  # Pour mettre à jour le modelClient dans le gestionnaire de portefeuille, si ouvert depuis le gestionnaire de portefeuille
        else:
            error = query.lastError().text()
            # ERROR
            detailed_message(self, QMessageBox.Critical, "Erreur de la base Access", "Échec de la suppression du client", error)

    def set_cbClient_portefeuille(self, cb):
        # Pour mettre à jour le modelClient dans le gestionnaire de portefeuille, si ouvert depuis le gestionnaire de portefeuille
        self.cbClient_portefeuille = cb

    def update_cbClient_portefeuille(self):
        # Pour mettre à jour le modelClient dans le gestionnaire de portefeuille, si ouvert depuis le gestionnaire de portefeuille
        if self.cbClient_portefeuille:
            self.cbClient_portefeuille.model().select()
            self.cbClient_portefeuille.setCurrentIndex(-1)
