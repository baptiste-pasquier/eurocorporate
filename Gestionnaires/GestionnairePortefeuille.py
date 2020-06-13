from PyQt5 import QtWidgets, uic, QtSql, QtCore
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtWidgets import QMessageBox, QDialogButtonBox, QProgressDialog
from Classes.client import Client
from Classes.portefeuille import Portefeuille
from Assistants.AddPortefeuille import WindowAddPortefeuille
from Assistants.ModifyPortefeuille import WindowModifyPortefeuille
from Tools import regex
import win32com.client as win32
import time
# qt_creator_file = "portefeuille.ui"
# Ui_MainWindowPortefeuille, QtBaseClass = uic.loadUiType(qt_creator_file)
from Gestionnaires import GestionnairePortefeuilleUI
from Gestionnaires.GestionnairePortefeuilleUI import Ui_MainWindowPortefeuille


class ModelClient(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Client')
        self.select()

    def data(self, index, role=Qt.DisplayRole):

        # Affichage noClient
        noClient_column = self.fieldIndex('noClient')
        nomEntreprise_column = self.fieldIndex('nomEntreprise')
        if role == Qt.DisplayRole and index.column() == noClient_column:
            noClient = super().data(index, Qt.DisplayRole)
            nomEntreprise = super().data(self.index(index.row(), nomEntreprise_column), Qt.DisplayRole)
            value = '{' + '{:0>2d}}} {}'.format(noClient, nomEntreprise)
            return value
        else:
            return super().data(index, role)


class ModelPortefeuille(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Portefeuille')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()

    def data(self, index, role=Qt.DisplayRole):

        # Affichage noPortefeuille
        noPortefeuille_column = self.fieldIndex('noPortefeuille')
        nomPortefeuille_column = self.fieldIndex('nomPortefeuille')
        if role == Qt.DisplayRole and index.column() == noPortefeuille_column:
            noPortefeuille = super().data(index, Qt.DisplayRole)
            nomPortefeuille = super().data(self.index(index.row(), nomPortefeuille_column), Qt.DisplayRole)
            value = '{' + '{:0>3d}}} {}'.format(noPortefeuille, nomPortefeuille)
            return value
        return super().data(index, role)


class ModelContenir(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Contenir')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.setSort(self.fieldIndex('ISIN'), Qt.AscendingOrder)
        self.select()

    def data(self, index, role=Qt.DisplayRole):

        if role == Qt.DisplayRole:
            # Affichage date
            if index.column() == self.fieldIndex('DateDeMAJ'):
                date = super().data(index, Qt.EditRole)
                value = date.toString("dd/MM/yyyy")
                return value

            if index.column() in [self.fieldIndex('nombre'), self.fieldIndex('prixAchat')]:
                nombre = super().data(index, Qt.EditRole)
                if nombre.is_integer():
                    value = str(int(nombre))
                else:
                    value = str((nombre))
                return value

        return super().data(index, role)


class ModelISIN(QtSql.QSqlQueryModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setQuery("SELECT DISTINCT ISIN, Libelle FROM Obligation ORDER BY ISIN ASC")
        self.setQuery("SELECT DISTINCT ISIN FROM Obligation ORDER BY ISIN ASC")
        while self.canFetchMore():
            self.fetchMore()


class MainWindowPortefeuille(QtWidgets.QMainWindow, Ui_MainWindowPortefeuille):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindowPortefeuille.__init__(self)
        self.setupUi(self)

        # self.db = createconnection()

        # crée le modèle et sa liaison avec la base SQL ouverte
        self.modelContenir = ModelContenir()

        # Lien entre la table graphique et le modèle
        self.tableView.setModel(self.modelContenir)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # self.tableView.selectionModel().selectionChanged.connect(self.change_mapper_index)
        self.tableView.selectionModel().selectionChanged.connect(self.selection_changed)
        self.indexRowSelected = -1

        # Liste des clients
        self.modelClient = ModelClient()
        self.clientChoisi = Client()

        self.comboBox_clients.setModel(self.modelClient)
        self.comboBox_clients.setModelColumn(self.modelClient.fieldIndex('noClient'))
        self.comboBox_clients.setCurrentIndex(-1)

        self.btn_chooseClient.clicked.connect(self.client_choose)
        self.btn_unlockClient.clicked.connect(self.client_unlock)
        self.btn_unlockClient.setEnabled(False)

        # Liste des portefeuilles
        self.modelPortefeuille = ModelPortefeuille()
        self.portefeuilleChoisi = Portefeuille()

        self.comboBox_portefeuilles.setModel(self.modelPortefeuille)
        self.comboBox_portefeuilles.setCurrentIndex(-1)
        self.comboBox_portefeuilles.setEnabled(False)

        self.btn_choosePortefeuille.clicked.connect(self.portefeuille_choose)
        self.btn_choosePortefeuille.setEnabled(False)

        self.btn_unlockPortefeuille.clicked.connect(self.portefeuille_unlock)
        self.btn_unlockPortefeuille.setEnabled(False)

        # Calendrier
        self.dateChoisie = self.calendarWidget.selectedDate()
        self.calendarWidget.selectionChanged.connect(self.date_changed)
        self.calendarWidget.setEnabled(False)

        # Toolbar
        self.action_deletePortefeuille.triggered.connect(self.delete_portefeuille)
        self.action_deletePortefeuille.setEnabled(False)
        self.action_modifyPortefeuilleName.triggered.connect(self.modify_portefeuille)
        self.action_modifyPortefeuilleName.setEnabled(False)

        # Table vide
        self.update_modelContenir()

        # Nouveau portefeuille
        self.btn_newPortefeuille.setEnabled(False)
        self.btn_newPortefeuille.clicked.connect(self.add_portefeuille)

        # Combobox ISIN
        self.modelISIN = ModelISIN()
        self.comboBox_ISIN.setModel(self.modelISIN)
        self.comboBox_ISIN.setModelColumn(0)
        self.comboBox_ISIN.setCurrentIndex(-1)
        self.comboBox_ISIN.currentIndexChanged.connect(self.comboBox_ISIN_changed)

        self.tb_dateChoisie.setEnabled(False)
        self.btn_today.setEnabled(False)
        self.btn_today.clicked.connect(lambda: self.calendarWidget.setSelectedDate(QDate.currentDate()))
        self.btn_search.setEnabled(False)
        self.comboBox_ISIN.setEnabled(False)
        self.tb_nombre.setEnabled(False)
        self.tb_prix.setEnabled(False)
        self.btn_modif.setEnabled(False)
        self.btn_suppr.setEnabled(False)
        self.btn_add.setEnabled(False)
        self.btn_vis.setEnabled(False)
        self.tb_valo.setEnabled(False)
        self.tb_valoAcqui.setEnabled(False)

        self.btn_add.clicked.connect(self.add_ligne)
        self.btn_modif.clicked.connect(self.modif_ligne)
        self.btn_suppr.clicked.connect(self.suppr_ligne)

        self.tb_nombre.textChanged.connect(self.tb_nombre_changed)
        self.tb_nombre_etat = False
        self.tb_prix.textChanged.connect(self.tb_prix_changed)
        self.tb_prix_etat = False
        self.tb_valo.textChanged.connect(self.tb_valo_changed)
        self.tb_valo_etat = False
        self.tb_valoAcqui.textChanged.connect(self.tb_valoAcqui_changed)
        self.tb_valoAcqui_etat = False

        # Liquidité
        self.tb_liquidite.setEnabled(False)
        self.tb_liquidite.textChanged.connect(self.tb_liquidite_changed)
        self.tb_liquidite_etat = False
        self.btn_liquidite.clicked.connect(self.liquidite_validate)
        self.btn_liquidite.setEnabled(False)

        self.color_error = "#FFCCCC"
        self.color_ok = "#CCE5FF"

        # Export import
        self.btn_export.clicked.connect(self.export)

    def client_choose(self):
        if self.comboBox_clients.currentIndex() >= 0:
            model = self.modelClient
            index = self.comboBox_clients.currentIndex()
            ID = model.index(index, model.fieldIndex('noClient')).data(Qt.EditRole)
            print('noClient = ', str(ID))

            self.clientChoisi.noClient = ID
            self.clientChoisi.get_values()

            self.btn_newPortefeuille.setEnabled(True)

            self.btn_unlockClient.setEnabled(True)
            self.btn_chooseClient.setEnabled(False)
            self.comboBox_clients.setEnabled(False)

            self.modelPortefeuille.setFilter('noClient = ' + str(self.clientChoisi.noClient))

            if self.modelPortefeuille.columnCount() > 0:
                self.btn_choosePortefeuille.setEnabled(True)
                self.comboBox_portefeuilles.setEnabled(True)
            else:
                self.btn_choosePortefeuille.setEnabled(False)
                self.comboBox_portefeuilles.setEnabled(False)
                QMessageBox.warning(self, '', "Aucun portefeuille créé pour le client choisi.")

        else:
            QMessageBox.warning(self, '', 'Veuillez choisir un client.')

    def client_unlock(self):
        self.btn_unlockClient.setEnabled(False)
        self.btn_chooseClient.setEnabled(True)
        self.comboBox_clients.setEnabled(True)
        self.btn_choosePortefeuille.setEnabled(False)
        self.comboBox_portefeuilles.setEnabled(False)
        self.comboBox_portefeuilles.setCurrentIndex(-1)

        self.clientChoisi = Client()

    def portefeuille_choose(self):
        if self.comboBox_portefeuilles.currentIndex() >= 0:
            self.btn_unlockPortefeuille.setEnabled(True)
            self.btn_unlockClient.setEnabled(False)
            self.comboBox_portefeuilles.setEnabled(False)
            self.action_deletePortefeuille.setEnabled(True)
            self.action_modifyPortefeuilleName.setEnabled(True)

            self.btn_choosePortefeuille.setEnabled(False)
            model = self.modelPortefeuille
            index = self.comboBox_portefeuilles.currentIndex()
            noPortefeuille = model.index(index, model.fieldIndex('noPortefeuille')).data(Qt.EditRole)
            print('noPortefeuille = ', str(noPortefeuille))
            self.portefeuilleChoisi.noPortefeuille = noPortefeuille
            self.portefeuilleChoisi.get_values()
            self.label_portefeuilleChoisi.setText('Portefeuille choisi : ' + model.index(index, model.fieldIndex('noPortefeuille')).data())

            datemax = self.update_calendar()
            self.calendarWidget.setSelectedDate(datemax)
            self.calendarWidget.setEnabled(True)
            self.date_changed()  # On force

            self.update_modelContenir()

            self.tb_dateChoisie.setEnabled(True)
            self.btn_today.setEnabled(True)
            self.btn_newPortefeuille.setEnabled(False)
            self.tb_liquidite.setEnabled(True)

            self.btn_search.setEnabled(True)
            self.comboBox_ISIN.setEnabled(True)
            self.btn_vis.setEnabled(True)

            self.btn_import.setEnabled(True)
            self.btn_export.setEnabled(True)

        else:
            QMessageBox.warning(self, '', 'Veuillez choisir un portefeuille.')

    def portefeuille_unlock(self):
        self.disable()

    def date_changed(self):
        self.dateChoisie = self.calendarWidget.selectedDate()
        print('Date : ' + self.dateChoisie.toString("dd/MM/yyyy"))
        self.tb_dateChoisie.setText(self.dateChoisie.toString("dd/MM/yyyy"))

        self.update_modelContenir()
        self.selection_changed()    # On force à cause de l'absence de selection
        self.comboBox_ISIN.setCurrentIndex(-1)
        self.comboBox_ISIN_changed()         # On force si on était déjà à -1

        self.affichage_liquidite()
        ####
        # A MODIFIER

        ####

    def update_modelContenir(self):
        self.modelContenir.setFilter('noPortefeuille = {} AND DateDeMAJ = #{}#'.format(self.portefeuilleChoisi.noPortefeuille, self.dateChoisie.toString("MM/dd/yyyy")))
        self.modelContenir.select()
        self.label_nbLignes.setText("Nombres de lignes : " + str(self.modelContenir.rowCount()))

    def selection_changed(self):
        select = self.tableView.selectionModel()
        if select.hasSelection():
            index = select.selectedRows()[0]
            self.indexRowSelected = index.row()
            model = self.modelContenir
            isin = str(model.record(index.row()).value("ISIN"))
            self.comboBox_ISIN.setCurrentText(isin)

            if self.comboBox_ISIN.currentText() != isin:
                self.comboBox_ISIN.setCurrentIndex(-1)
                self.comboBox_ISIN_changed()

            self.btn_modif.setEnabled(True)
            self.btn_suppr.setEnabled(True)
        else:
            self.indexRowSelected = -1
            self.btn_modif.setEnabled(False)
            self.btn_suppr.setEnabled(False)

        print('indexRowSelected = ', str(self.indexRowSelected))

    def add_portefeuille(self):
        def textchanged():
            if regex.VerifAdresse(dialog.tb_libelle.text()):
                query = QtSql.QSqlQuery()
                query.exec("SELECT count(*) FROM Portefeuille WHERE nomPortefeuille = '" + dialog.tb_libelle.text() + "' AND noClient = " + str(self.clientChoisi.noClient))
                if query.next():
                    compteur = int(query.value(0))
                query.clear()
                if compteur == 0:
                    dialog.tb_message.setText("...")
                    dialog.tb_libelle.setStyleSheet("background : " + self.color_ok)
                    dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
                else:
                    dialog.tb_message.setText("Un portefeuille porte déjà ce nom.")
                    dialog.tb_libelle.setStyleSheet("background : " + self.color_error)
                    dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            else:
                dialog.tb_message.setText("Format incorrect.")
                dialog.tb_libelle.setStyleSheet("background : " + self.color_error)
                dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        dialog = WindowAddPortefeuille(self)
        dialog.tb_client.setText(self.clientChoisi.nomEntreprise)
        dialog.tb_message.setText("Définir un libellé.")
        dialog.tb_libelle.setStyleSheet("background : " + self.color_error)
        dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        dialog.tb_libelle.textEdited.connect(textchanged)

        if dialog.exec() == QtWidgets.QDialog.Accepted:
            nom_portefeuille = dialog.tb_libelle.text()

            model = self.modelPortefeuille
            new_row = model.record()

            # Nouveau numéro du portefeuille
            query = QtSql.QSqlQuery()
            query.exec("SELECT MAX(noPortefeuille) FROM Portefeuille")
            if query.next():
                max_no_portefeuille = int(query.value(0))
            query.clear()

            defaults = {
                'noPortefeuille': max_no_portefeuille + 1,
                'noClient': self.clientChoisi.noClient,
                'nomPortefeuille': nom_portefeuille
            }

            for field, value in defaults.items():
                index = model.fieldIndex(field)
                new_row .setValue(index, value)

            resul = model.insertRecord(-1, new_row)
            if not resul:
                error = model.lastError().text()
                QMessageBox.critical(self, "Python error", "Insert failed : " + error)
            else:
                if model.submitAll():
                    QMessageBox.information(self, "Nouveau portefeuille", "Ajout réussi")
                else:
                    error = model.lastError().text()
                    QMessageBox.critical(self, "Database error", "Insert failed : " + error)
                    model.select()

            self.comboBox_portefeuilles.setEnabled(True)
            self.btn_choosePortefeuille.setEnabled(True)
            self.btn_unlockClient.setEnabled(True)

        else:
            QMessageBox.information(self, "Nouveau portefeuille", "Ajout annulé")

    def modify_portefeuille(self):
        def textchanged():
            if regex.VerifAdresse(dialog.tb_nouvLibelle.text()):
                query = QtSql.QSqlQuery()
                query.exec("SELECT count(*) FROM Portefeuille WHERE nomPortefeuille = '" + dialog.tb_nouvLibelle.text() + "' AND noClient = " + str(self.clientChoisi.noClient))
                if query.next():
                    compteur = int(query.value(0))
                query.clear()
                if compteur == 0:
                    dialog.tb_message.setText("...")
                    dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
                else:
                    dialog.tb_message.setText("Un portefeuille porte déjà ce nom.")
                    dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            else:
                dialog.tb_message.setText("Format incorrect.")
                dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        dialog = WindowModifyPortefeuille(self)
        dialog.tb_client.setText(self.clientChoisi.nomEntreprise)
        dialog.tb_ancienLibelle.setText(self.portefeuilleChoisi.nomPortefeuille)
        dialog.tb_message.setText("Définir un nouveau libellé.")
        dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        dialog.tb_nouvLibelle.textEdited.connect(textchanged)

        if dialog.exec() == QtWidgets.QDialog.Accepted:
            nouv_nom_portefeuille = dialog.tb_nouvLibelle.text()

            query = QtSql.QSqlQuery()
            resul = query.exec("UPDATE Portefeuille SET nomPortefeuille = '" + nouv_nom_portefeuille + "' WHERE noPortefeuille = " + str(self.portefeuilleChoisi.noPortefeuille))

            if resul:
                QMessageBox.information(self, "Modification portefeuille", "Modification réussie")
            else:
                error = query.lastError().text()
                QMessageBox.critical(self, "Database error", "Modification failed : " + error)

            self.portefeuilleChoisi.get_values()
            self.label_portefeuilleChoisi.setText("Portefeuille choisie : " + self.portefeuilleChoisi.nomPortefeuille)
            index = self.comboBox_portefeuilles.currentIndex()
            self.modelPortefeuille.select()
            self.comboBox_portefeuilles.setCurrentIndex(index)

        else:
            QMessageBox.information(self, "Modification portefeuille", "Modification annulée")

    def delete_portefeuille(self):
        reply = QMessageBox.warning(self, 'Suppression', "Êtes vous sûr de vouloir supprimer ce portefeuille?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            query = QtSql.QSqlQuery()
            resul1 = query.exec("DELETE FROM Contenir WHERE noPortefeuille = " + str(self.portefeuilleChoisi.noPortefeuille))
            resul2 = query.exec("DELETE FROM Portefeuille WHERE noPortefeuille = " + str(self.portefeuilleChoisi.noPortefeuille))
            if resul1 and resul2:
                QMessageBox.information(self, "Suppresion", "Suppression réussie")
            else:
                error = query.lastError().text()
                QMessageBox.critical(self, "Database error", "Delete failed : " + error)

            self.modelPortefeuille.select()
            self.comboBox_portefeuilles.setCurrentIndex(-1)

            self.disable()

        else:
            QMessageBox.information(self, "Suppresion", "Suppression annulée")

    def add_ligne(self):
        model = self.modelContenir
        new_row = model.record()

        if self.tb_nombre.isEnabled:
            nbOrValo = self.tb_nombre.text()
            prixOrValoAC = self.tb_prix.text()
        else:
            nbOrValo = self.tb_valo.text()
            prixOrValoAC = self.tb_valoAcqui.text()

        noPort = self.portefeuilleChoisi.noPortefeuille
        Isin = self.comboBox_ISIN.currentText()

        defaults = {
            'noPortefeuille': int(noPort),
            'ISIN': str(Isin),
            'DateDeMAJ': self.dateChoisie
        }

        if self.tb_prix.isEnabled:
            defaults['Nombre'] = float(self.tb_nombre.text())
            defaults['PrixAchat'] = float(self.tb_prix.text())
        else:
            defaults['Valorisation'] = float(self.tb_valo.text())
            defaults['ValorisationAC'] = float(self.tb_valoAcqui.text())

        for field, value in defaults.items():
            index = model.fieldIndex(field)
            new_row .setValue(index, value)

        resul = model.insertRecord(-1, new_row)
        if not resul:
            error = model.lastError().text()
            QMessageBox.critical(self, "Python error", "Insert failed : " + error)
        else:
            if model.submitAll():
                QMessageBox.information(self, "Nouvelle ligne", "Ajout réussi")
            else:
                error = model.lastError().text()
                QMessageBox.critical(self, "Database error", "Insert failed : " + error)
                model.select()

        self.update_modelContenir()
        self.RajoutObligDateFutur(Isin, noPort, nbOrValo, prixOrValoAC)
        self.update_modelContenir()
        # On a déjà indexRowSelected = -1
        self.comboBox_ISIN.setCurrentIndex(-1)
        self.update_calendar()

    def RajoutObligDateFutur(self, Isin, noPort, nbOrValo, prixOrValoAC):
        # On va ajouter dans les jours suivants l'Obligation pour chaque date de valorisation
        listDate = []
        query = QtSql.QSqlQuery()
        query.exec("SELECT DISTINCT DateDeMAJ FROM Contenir WHERE noPortefeuille = " + str(noPort) + " AND DateDeMAJ > #" + self.dateChoisie.toString("MM/dd/yyyy") + "#")
        while query.next():
            listDate.append(query.value(0).date())
        query.clear()

        for date in listDate:
            query = QtSql.QSqlQuery()
            query.exec("SELECT count(*) FROM Contenir WHERE noPortefeuille = " + str(noPort) + " AND DateDeMAJ = #" + date.toString("MM/dd/yyyy") + "# AND ISIN = '" + Isin + "'")
            if query.next():
                count = int(query.value(0))

            # On vérifie si elle existe déjà, si oui on l'update (1)
            if count == 1:
                if self.tb_nombre.isEnabled:  # Si c'est pas une structure
                    query = QtSql.QSqlQuery()
                    resul = query.exec("UPDATE Contenir SET nombre = '" + nbOrValo + "', prixAchat = '" + prixOrValoAC + "' WHERE noPortefeuille = " + str(noPort) + " AND DateDeMAJ = #" + date.toString("MM/dd/yyyy") + "# AND ISIN = '" + Isin + "'")
                else:
                    query = QtSql.QSqlQuery()
                    resul = query.exec("UPDATE Contenir SET Valorisation = '" + nbOrValo + "', ValorisationAC = '" + prixOrValoAC + "' WHERE noPortefeuille = " + str(noPort) + " AND DateDeMAJ = #" + date.toString("MM/dd/yyyy") + "# AND ISIN = '" + Isin + "'")

                if resul:
                    QMessageBox.information(self, "Date future", "Mise à jour à la date future : " + date.toString("dd/MM/yyyy"))
                else:
                    error = query.lastError().text()
                    QMessageBox.critical(self, "Database error", "Update failed : " + error)

            else:
                if self.tb_nombre.isEnabled:  # Si c'est pas une structure
                    query = QtSql.QSqlQuery()
                    resul = query.exec("INSERT INTO Contenir (noPortefeuille, ISIN, DateDeMAJ, nombre, prixAchat) VALUES (" + str(noPort) + ",'" + Isin + "',#" + date.toString("MM/dd/yyyy") + "#, '" + nbOrValo + "','" + prixOrValoAC + "')")
                else:
                    query = QtSql.QSqlQuery()
                    resul = query.exec("INSERT INTO Contenir (noPortefeuille, ISIN, DateDeMAJ, Valorisation, ValorisationAC) VALUES (" + str(noPort) + ",'" + Isin + "',#" + date.toString("MM/dd/yyyy") + "#, '" + nbOrValo + "','" + prixOrValoAC + "')")

                if resul:
                    QMessageBox.information(self, "Date future", "Ajout à la date future : " + date.toString("dd/MM/yyyy"))
                else:
                    error = query.lastError().text()
                    QMessageBox.critical(self, "Database error", "Insert failed : " + error)

    def modif_ligne(self):
        model = self.modelContenir
        new_row = model.record()

        if self.tb_nombre.isEnabled:
            nbOrValo = self.tb_nombre.text()
            prixOrValoAC = self.tb_prix.text()
        else:
            nbOrValo = self.tb_valo.text()
            prixOrValoAC = self.tb_valoAcqui.text()

        noPort = self.portefeuilleChoisi.noPortefeuille
        row = self.indexRowSelected
        isin = str(model.record(row).value('ISIN'))

        defaults = {
            'noPortefeuille': int(noPort),
            'ISIN': str(isin),
            'DateDeMAJ': self.dateChoisie
        }

        if self.tb_prix.isEnabled:
            defaults['Nombre'] = float(self.tb_nombre.text())
            defaults['PrixAchat'] = float(self.tb_prix.text())
        else:
            defaults['Valorisation'] = float(self.tb_valo.text())
            defaults['ValorisationAC'] = float(self.tb_valoAcqui.text())

        for field, value in defaults.items():
            index = model.fieldIndex(field)
            new_row.setValue(index, value)

        resul = model.setRecord(row, new_row)
        if not resul:
            error = model.lastError().text()
            QMessageBox.critical(self, "Python error", "Modification failed : " + error)
        else:
            if model.submitAll():
                QMessageBox.information(self, "Modification ligne", "Modification réussie")
            else:
                error = model.lastError().text()
                QMessageBox.critical(self, "Database error", "Modification failed : " + error)
                model.select()

        self.update_modelContenir()
        self.RajoutObligDateFutur(isin, noPort, nbOrValo, prixOrValoAC)
        self.update_modelContenir()
        self.tableView.selectRow(row)

    def suppr_ligne(self):
        model = self.modelContenir
        reply = QMessageBox.warning(self, 'Suppression', "Êtes vous sûr de vouloir supprimer la ligne sélectionnée ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            resul = model.removeRows(self.indexRowSelected, 1)
            if not resul:
                error = model.lastError().text()
                QMessageBox.critical(self, "Python error", "Delete failed : " + error)
            else:
                if model.submitAll():
                    QMessageBox.information(self, "Suppression de ligne", "Suppression réussie")
                else:
                    error = model.lastError().text()
                    QMessageBox.critical(self, "Database error", "Delete failed : " + error)
                    model.select()

            self.update_modelContenir()
            self.tableView.clearSelection()
            self.selection_changed()
            self.comboBox_ISIN.setCurrentIndex(-1)
            self.update_calendar()

    def tb_nombre_changed(self):
        try:
            float(self.tb_nombre.text())
            test = True
        except ValueError:
            test = False

        if test:
            self.tb_nombre.setStyleSheet("background : " + self.color_ok)
            self.tb_nombre_etat = True
        else:
            self.tb_nombre.setStyleSheet("background : " + self.color_error)
            self.tb_nombre_etat = False
        self.verif()

    def tb_prix_changed(self):
        try:
            float(self.tb_prix.text())
            test = True
        except ValueError:
            test = False

        if test:
            self.tb_prix.setStyleSheet("background : " + self.color_ok)
            self.tb_prix_etat = True
        else:
            self.tb_prix.setStyleSheet("background : " + self.color_error)
            self.tb_prix_etat = False
        self.verif()

    def verif(self):
        if self.tb_nombre_etat and self.tb_prix_etat:
            if self.indexRowSelected > -1:
                self.btn_modif.setEnabled(True)
            else:
                self.btn_add.setEnabled(True)
        else:
            self.btn_modif.setEnabled(False)
            self.btn_add.setEnabled(False)

    def tb_valo_changed(self):
        try:
            float(self.tb_valo.text())
            test = True
        except ValueError:
            test = False

        if test:
            self.tb_valo.setStyleSheet("background : " + self.color_ok)
            self.tb_valo_etat = True
        else:
            self.tb_valo.setStyleSheet("background : " + self.color_error)
            self.tb_valo_etat = False
        self.verif_valo()

    def tb_valoAcqui_changed(self):
        try:
            float(self.tb_valoAcqui.text())
            test = True
        except ValueError:
            test = False

        if test:
            self.tb_valoAcqui.setStyleSheet("background : " + self.color_ok)
            self.tb_valoAcqui_etat = True
        else:
            self.tb_valoAcqui.setStyleSheet("background : " + self.color_error)
            self.tb_valoAcqui_etat = False
        self.verif_valo()

    def verif_valo(self):
        if self.tb_valo_etat and self.tb_valoAcqui_etat:
            if self.indexRowSelected > -1:
                self.btn_modif.setEnabled(True)
            else:
                self.btn_add.setEnabled(True)
        else:
            self.btn_modif.setEnabled(False)
            self.btn_add.setEnabled(False)

    def comboBox_ISIN_changed(self):
        self.tb_nombre.setText("")
        self.tb_prix.setText("")
        self.tb_valo.setText("")
        self.tb_valoAcqui.setText("")
        self.label_libelle.setText("")
        self.label_dateMAJ.setText("")
        self.label_nominal.setText("")
        self.tb_nombre.setStyleSheet("")
        self.tb_prix.setStyleSheet("")
        self.tb_valo.setStyleSheet("")
        self.tb_valoAcqui.setStyleSheet("")
        self.tb_nombre.setEnabled(False)
        self.tb_prix.setEnabled(False)
        self.tb_valo.setEnabled(False)
        self.tb_valoAcqui.setEnabled(False)

        model = self.modelContenir
        isin_bool = False   # Si on travaille sur une obligation
        struct = False
        in_base_obligation = False  # Si l'obligation est dans la base Obligation
        in_table = False  # Si l'obligation est dans la table

        if self.comboBox_ISIN.currentIndex() > -1:
            # Cas où on sélectionne directement un ISIN, ou si on a sélectionné une ligne du tableau et arrivé ici
            isin = self.comboBox_ISIN.currentText()
            isin_bool = True
            in_base_obligation = True

            # On vérifie le type de l'obligation
            query = QtSql.QSqlQuery()
            query.exec("SELECT noType FROM Obligation WHERE ISIN = '" + isin + "'")
            if query.next():
                notype = int(query.value(0))
            query.clear()
            if notype == 2:  # Structuré
                struct = True

            # On vérifie si l'obligation est dans le tableau et on sélectionne la ligne
            i = 0
            while i < model.rowCount() and in_table is False:
                if str(model.record(i).value("ISIN")) == isin:
                    self.tableView.selectRow(i)
                    in_table = True
                i += 1

        elif self.indexRowSelected > -1:
            # Cas où on sélectionne une ligne dans le tableau non présente dans la combobox
            in_table = True
            isin = str(self.modelContenir.record(self.indexRowSelected).value("ISIN"))
            isin_bool = True

        if struct:
            # Si obligation structurée
            self.tb_valo.setEnabled(True)
            self.tb_valoAcqui.setEnabled(True)
            self.tb_valo_changed()
            self.tb_valoAcqui_changed()
        elif isin_bool:
            # Si obligation non structurée
            self.tb_nombre.setEnabled(True)
            self.tb_prix.setEnabled(True)
            self.tb_nombre_changed()
            self.tb_prix_changed()

        if in_base_obligation:
            # Si obligation dans la base obligation
            query = QtSql.QSqlQuery()
            query.exec("SELECT Nominal, DateDeMAJ, Libelle FROM Obligation WHERE ISIN = '" + isin + "' ORDER BY DateDeMAJ DESC")
            if query.next():
                self.label_nominal.setText(str(query.value(0)))
                self.label_dateMAJ.setText(query.value(1).toString("dd/MM/yyyy"))
                self.label_libelle.setText(str(query.value(2)))
        elif isin_bool:
            # Si obligation non dans la base obligation
            self.label_nominal.setText("ISIN inconnu")
            self.label_dateMAJ.setText("ISIN inconnu")
            self.label_libelle.setText("ISIN inconnu")

        if in_table:
            # Si obligation dans la table
            index = self.indexRowSelected
            if struct:
                self.tb_valo.setText(str(model.record(index).value("Valorisation")))
                self.tb_valoAcqui.setText(str(model.record(index).value("ValorisationAC")))
            else:
                self.tb_nombre.setText(str(model.record(index).value("nombre")))
                self.tb_prix.setText(str(model.record(index).value("prixAchat")))
        elif isin_bool:
            # Si obligation non dans la table
            self.tableView.clearSelection()

    def update_calendar(self):
        noPortefeuille = self.portefeuilleChoisi.noPortefeuille

        if noPortefeuille:
            # Dates de mise à jour
            query = QtSql.QSqlQuery()
            query.exec("SELECT DISTINCT DateDeMAJ FROM Contenir WHERE noPortefeuille = " + str(noPortefeuille) + " ORDER BY DateDeMAJ ASC")
            datemax = QDate.currentDate()
            while query.next():
                datemax = query.value(0).date()
                self.calendarWidget.highlight.append(datemax)
            query.clear()
            return datemax
        else:
            self.calendarWidget.highlight = []

    def affichage_liquidite(self):
        self.tb_liquidite.setText("")
        query = QtSql.QSqlQuery()
        query.exec("SELECT count(*) FROM Liquidite WHERE noPortefeuille = {} AND DateDeMAJ = #{}#".format(self.portefeuilleChoisi.noPortefeuille, self.dateChoisie.toString("MM/dd/yyyy")))
        if query.next():
            compteur = int(query.value(0))
        else:
            compteur = -1
        query.clear()

        if compteur == 1:
            query = QtSql.QSqlQuery()
            query.exec("SELECT Liquidite FROM Liquidite WHERE noPortefeuille = {} AND DateDeMAJ = #{}#".format(self.portefeuilleChoisi.noPortefeuille, self.dateChoisie.toString("MM/dd/yyyy")))
            if query.next():
                self.tb_liquidite.setText(str(query.value(0)))
            query.clear()

        self.tb_liquidite_changed()

    def liquidite_validate(self):
        query = QtSql.QSqlQuery()
        resul1 = query.exec("DELETE FROM Liquidite WHERE noPortefeuille = {} AND DateDeMAJ = #{}#".format(self.portefeuilleChoisi.noPortefeuille, self.dateChoisie.toString("MM/dd/yyyy")))
        resul2 = query.exec("INSERT INTO Liquidite (noPortefeuille, DateDeMAJ, Liquidite) VALUES ({}, #{}#, '{}')".format(self.portefeuilleChoisi.noPortefeuille, self.dateChoisie.toString("MM/dd/yyyy"), self.tb_liquidite.text()))
        query.clear()
        if resul1 and resul2:
            QMessageBox.information(self, "Modification liquidité", "Modification réussie")
        else:
            QMessageBox.critical(self, "Modification liquidité", "Modification non réussie")

    def tb_liquidite_changed(self):
        try:
            float(self.tb_liquidite.text())
            test = True
        except ValueError:
            test = False

        if test:
            self.tb_liquidite.setStyleSheet("background : " + self.color_ok)
            self.tb_liquidite_etat = False
            self.btn_liquidite.setEnabled(True)
        else:
            self.tb_liquidite.setStyleSheet("background : " + self.color_error)
            self.tb_liquidite_etat = True
            self.btn_liquidite.setEnabled(False)

    def disable(self):
        self.btn_unlockPortefeuille.setEnabled(False)
        self.btn_unlockClient.setEnabled(True)
        self.comboBox_portefeuilles.setEnabled(True)
        self.action_deletePortefeuille.setEnabled(False)
        self.action_modifyPortefeuilleName.setEnabled(False)

        self.btn_choosePortefeuille.setEnabled(True)
        self.portefeuilleChoisi = Portefeuille()
        self.label_portefeuilleChoisi.setText('Portefeuille choisi : ')

        self.calendarWidget.setSelectedDate(QDate.currentDate())
        self.calendarWidget.setEnabled(False)
        self.update_calendar()
        self.date_changed()

        self.tb_dateChoisie.setEnabled(False)
        self.tb_dateChoisie.setText("")
        self.btn_today.setEnabled(False)
        self.tb_liquidite.setText("")
        self.tb_liquidite.setStyleSheet("")
        self.tb_liquidite.setEnabled(False)

        self.btn_search.setEnabled(False)
        self.comboBox_ISIN.setEnabled(False)
        self.btn_vis.setEnabled(False)

        self.btn_import.setEnabled(False)
        self.btn_export.setEnabled(False)

    def export(self):
        query = QtSql.QSqlQuery()
        query.exec("SELECT COUNT(*) FROM Valorisation WHERE noPortefeuille = " + str(self.portefeuilleChoisi.noPortefeuille) + " AND DateDeMAJ = #" + self.dateChoisie.toString("MM/dd/yyyy") + "#")
        nb_lignes = 0
        if query.next():
            nb_lignes = int(query.value(0))

        if nb_lignes != 0:
            progress = QProgressDialog("Chargement des données", "Annuler", 2, nb_lignes + 3, self)
            progress.setWindowTitle("Exportation")
            progress.setWindowModality(Qt.WindowModal)
            progress.show()

            query.exec("SELECT ISIN, Libelle, Emetteur, Maturite, Coupon, Nominal, Cours, Rating, dateDeMAJ, MAJ, nombre, PrixAchat, Rendement, Duration, Sensibilite, Convexite, VieMoyenne, nomRegion, nomType, nomSection, nomSousSecteur, SpreadASW, SpreadBund, ClasseDuration, RatingSP, Valorisation, ValorisationAC, [Valeur d'acquisition], [Valo par le prix], Remboursement, [+ ou - value], [+ ou - value %] FROM  Valorisation WHERE [noPortefeuille] = " + str(self.portefeuilleChoisi.noPortefeuille) + " AND DateDeMAJ = #" + self.dateChoisie.toString("MM/dd/yyyy") + "#")
            progress.setLabelText("Transfert vers Excel")

            xls = win32.Dispatch('Excel.Application')

            # Paramètres
            # xls.WindowState = Excel.XlWindowState.xlMaximized  # format plein écran
            xls.ShowWindowsInTaskbar = True  # visible dans la barre de tâches
            xls.DisplayFormulaBar = True  # affichage de la barre de formule
            xls.Caption = "Portefeuille " + self.portefeuilleChoisi.nomPortefeuille
            wb = xls.Workbooks.Add()  # ajout d'un classeur Excel
            xls.Worksheets(1).Name = "Portefeuille"
            xls.Worksheets(1).Rows("1").Font.Bold = True

            # Entête de colonne
            xls.Worksheets(1).Range("A1").Value = "ISIN"
            xls.Worksheets(1).Range("B1").Value = "Libelle"
            xls.Worksheets(1).Range("C1").Value = "Emetteur"
            xls.Worksheets(1).Range("D1").Value = "Maturite"
            xls.Worksheets(1).Range("E1").Value = "Coupon"
            xls.Worksheets(1).Range("F1").Value = "Nominal"
            xls.Worksheets(1).Range("G1").Value = "Cours"
            xls.Worksheets(1).Range("H1").Value = "Rating"
            xls.Worksheets(1).Range("I1").Value = "+ ou - value %"
            xls.Worksheets(1).Range("J1").Value = "dateDeMAJ"
            xls.Worksheets(1).Range("K1").Value = "MAJ"
            xls.Worksheets(1).Range("L1").Value = "nombre"
            xls.Worksheets(1).Range("M1").Value = "PrixAchat"
            xls.Worksheets(1).Range("N1").Value = "Rendement"
            xls.Worksheets(1).Range("O1").Value = "Duration"
            xls.Worksheets(1).Range("P1").Value = "Sensibilite"
            xls.Worksheets(1).Range("Q1").Value = "Convexite"
            xls.Worksheets(1).Range("R1").Value = "VieMoyenne"
            xls.Worksheets(1).Range("S1").Value = "nomRegion"
            xls.Worksheets(1).Range("T1").Value = "nomType"
            xls.Worksheets(1).Range("U1").Value = "nomSection"
            xls.Worksheets(1).Range("V1").Value = "nomSousSecteur"
            xls.Worksheets(1).Range("W1").Value = "SpreadASW"
            xls.Worksheets(1).Range("X1").Value = "SpreadBund"
            xls.Worksheets(1).Range("Y1").Value = "ClasseDuration"
            xls.Worksheets(1).Range("Z1").Value = "RatingSP"
            xls.Worksheets(1).Range("AA1").Value = "Valorisation"
            xls.Worksheets(1).Range("AB1").Value = "ValorisationAC"
            xls.Worksheets(1).Range("AC1").Value = "Valeur d'acquisition"
            xls.Worksheets(1).Range("AD1").Value = "Valo par le prix"
            xls.Worksheets(1).Range("AE1").Value = "Remboursement"
            xls.Worksheets(1).Range("AF1").Value = "+ ou - value"

            nb_col = 32
            ligne = 2

            break_bool = False
            while query.next():
                QtCore.QCoreApplication.processEvents()
                progress.setValue(ligne)
                for i in range(1, nb_col + 1):
                    value = query.value(str(xls.Worksheets(1).Cells(1, i).Value))
                    if isinstance(value, QtCore.QDateTime) or isinstance(value, QtCore.QDate):
                        resul = value.toString("MM/dd/yyyy")
                        # resul = str(value)
                    elif isinstance(value, float):
                        resul = float(value)
                    elif isinstance(value, int):
                        resul = int(value)
                    else:
                        resul = str(value)
                    xls.Worksheets(1).Cells(ligne, i).Value = resul
                if progress.wasCanceled():
                    break_bool = True
                    break
                ligne += 1

            progress.setValue(nb_lignes + 3)
            query.clear()

            if not break_bool:
                QMessageBox.information(self, "Exportation", "Exportation terminée")
                xls.Worksheets(1).Columns("A:AG").EntireColumn.AutoFit()
                xls.Visible = True
            else:
                QMessageBox.warning(self, "Exportation", "Exportation annulée")
                xls.DisplayAlerts = False
                map(lambda book: book.Close(False), xls.Workbooks)
                xls.Quit()

        else:
            QMessageBox.warning(self, "Exportation", "Aucune valeur")
