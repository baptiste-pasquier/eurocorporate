from PyQt5 import QtWidgets, uic, QtSql, QtCore
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QMessageBox, QDialogButtonBox
from Classes.client import Client
from Classes.portefeuille import Portefeuille
from Assistants.AddPortefeuille import WindowAddPortefeuille
from Assistants.ModifyPortefeuille import WindowModifyPortefeuille
from Tools import regex

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
        self.comboBox_ISIN.currentIndexChanged.connect(self.Isin_changed)

        # # Mapping table
        # self.mapper = QtWidgets.QDataWidgetMapper(self)
        # self.mapper.setModel(self.modelContenir)
        # self.mapper.addMapping(self.comboBox_ISIN, self.modelContenir.fieldIndex('ISIN'))
        # self.mapper.addMapping(self.tb_nombre, self.modelContenir.fieldIndex('nombre'))
        # self.mapper.addMapping(self.tb_prix, self.modelContenir.fieldIndex('prixAchat'))

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
        # self.btn_modif.clicked.connect(self.modif_ligne)
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
        # self.btn_newPortefeuille.setEnabled(False)
        # self.action_deletePortefeuille.setEnabled(False)
        # self.label_portefeuilleChoisi.setText('Portefeuille choisi : ')
        #
        #
        # self.btn_search.setEnabled(False)
        # self.comboBox_ISIN.setEnabled(False)
        # self.tb_nombre.setEnabled(False)
        # self.tb_prix.setEnabled(False)
        # self.btn_modif.setEnabled(False)
        # self.btn_suppr.setEnabled(False)
        # self.btn_add.setEnabled(False)
        # self.btn_import.setEnabled(False)
        # self.btn_export.setEnabled(False)

        self.clientChoisi = Client()

    def portefeuille_choose(self):
        if self.comboBox_portefeuilles.currentIndex() >= 0:
            self.calendarWidget.setSelectedDate(QDate.currentDate())

            self.calendarWidget.setEnabled(True)
            self.action_deletePortefeuille.setEnabled(True)
            self.btn_import.setEnabled(True)

            model = self.modelPortefeuille
            index = self.comboBox_portefeuilles.currentIndex()
            noPortefeuille = model.index(index, model.fieldIndex('noPortefeuille')).data(Qt.EditRole)
            print('noPortefeuille = ', str(noPortefeuille))
            self.portefeuilleChoisi.noPortefeuille = noPortefeuille
            self.portefeuilleChoisi.get_values()
            self.label_portefeuilleChoisi.setText('Portefeuille choisi : ' + model.index(index, model.fieldIndex('noPortefeuille')).data())

            datemax = self.update_calendar()

            self.calendarWidget.setSelectedDate(datemax)
            self.date_changed()  # On force

            self.update_modelContenir()
            self.btn_choosePortefeuille.setEnabled(False)

            self.btn_search.setEnabled(True)
            self.comboBox_ISIN.setEnabled(True)
            self.tb_nombre.setEnabled(True)
            self.tb_prix.setEnabled(True)
            self.comboBox_portefeuilles.setEnabled(False)
            self.btn_unlockPortefeuille.setEnabled(True)
            self.btn_add.setEnabled(False)
            self.btn_unlockClient.setEnabled(False)
            self.btn_vis.setEnabled(True)
            self.action_modifyPortefeuilleName.setEnabled(True)
            self.btn_export.setEnabled(True)

            self.tb_dateChoisie.setEnabled(True)
            self.btn_today.setEnabled(True)
            self.btn_newPortefeuille.setEnabled(False)
            self.tb_liquidite.setEnabled(True)

        else:
            QMessageBox.warning(self, '', 'Veuillez choisir un portefeuille.')

    def portefeuille_unlock(self):
        self.btn_unlockPortefeuille.setEnabled(False)
        self.comboBox_portefeuilles.setEnabled(True)
        self.action_deletePortefeuille.setEnabled(False)
        self.btn_add.setEnabled(False)
        self.btn_modif.setEnabled(False)
        self.btn_suppr.setEnabled(False)
        self.btn_unlockClient.setEnabled(True)
        self.action_modifyPortefeuilleName.setEnabled(False)
        self.btn_import.setEnabled(False)
        self.btn_export.setEnabled(False)
        self.calendarWidget.setSelectedDate(QDate.currentDate())
        self.calendarWidget.setEnabled(False)

        self.btn_choosePortefeuille.setEnabled(True)
        self.portefeuilleChoisi = Portefeuille()

        self.update_calendar()

        self.label_portefeuilleChoisi.setText('Portefeuille choisi : ')
        self.update_modelContenir()
        self.selection_changed()    # On force si on était déjà à -1
        self.comboBox_ISIN.setCurrentIndex(-1)
        self.Isin_changed()
        self.btn_search.setEnabled(False)
        self.comboBox_ISIN.setEnabled(False)
        self.tb_nombre.setEnabled(False)
        self.tb_prix.setEnabled(False)
        self.btn_vis.setEnabled(False)

        self.tb_dateChoisie.setEnabled(False)
        self.tb_dateChoisie.setText("")
        self.btn_today.setEnabled(False)
        self.tb_liquidite.setText("")
        self.tb_liquidite.setStyleSheet("")
        self.tb_liquidite.setEnabled(False)

    def date_changed(self):
        self.dateChoisie = self.calendarWidget.selectedDate()
        print('Date : ' + self.dateChoisie.toString("dd/MM/yyyy"))
        self.tb_dateChoisie.setText(self.dateChoisie.toString("dd/MM/yyyy"))

        self.update_modelContenir()
        self.selection_changed()    # On force si on était déjà à -1
        self.comboBox_ISIN.setCurrentIndex(-1)
        self.Isin_changed()         # On force si on était déjà à -1

        self.affichage_liquidite()
        ####
        # A MODIFIER

        ####

    def update_modelContenir(self):
        # self.modelContenir.setFilter('noPortefeuille = {}'.format(self.portefeuilleChoisi.noPortefeuille))
        self.modelContenir.setFilter('noPortefeuille = {} AND DateDeMAJ = #{}#'.format(self.portefeuilleChoisi.noPortefeuille, self.dateChoisie.toString("MM/dd/yyyy")))
        self.modelContenir.select()
        self.label_nbLignes.setText("Nombres de lignes : " + str(self.modelContenir.rowCount()))

    # def change_mapper_index(self):
    #     select = self.tableView.selectionModel()
    #     if select.hasSelection():
    #         index = select.selectedRows()[0]
    #         self.mapper.setCurrentModelIndex(index)

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

            self.btn_modif.setEnabled(True)
            self.btn_suppr.setEnabled(True)
            self.btn_add.setEnabled(False)
        else:
            self.indexRowSelected = -1
            self.btn_modif.setEnabled(False)
            self.btn_suppr.setEnabled(False)
            self.btn_add.setEnabled(False)

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

            self.portefeuilleChoisi = Portefeuille()
            self.label_portefeuilleChoisi.setText("Portefeuille choisi :")
            self.action_deletePortefeuille.setEnabled(False)
            self.btn_unlockPortefeuille.setEnabled(False)
            self.comboBox_portefeuilles.setEnabled(True)
            self.btn_add.setEnabled(False)
            self.btn_modif.setEnabled(False)
            self.btn_suppr.setEnabled(False)
            self.btn_unlockClient.setEnabled(True)
            self.action_modifyPortefeuilleName.setEnabled(False)
            self.comboBox_portefeuilles.setCurrentIndex(-1)

            self.btn_choosePortefeuille.setEnabled(True)
            self.modelPortefeuille.select()
        else:
            QMessageBox.information(self, "Suppresion", "Suppression annulée")

    def add_ligne(self):
        if self.comboBox_ISIN.currentIndex() > -1 and self.tb_nombre_etat and self.tb_prix_etat:

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
            self.comboBox_ISIN.setCurrentIndex(-1)
            self.update_calendar()

        else:
            QMessageBox.information(self, "Ajout", "Ajout impossible: remplir le formulaire")

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

    def suppr_ligne(self):
        model = self.modelContenir
        # if self.indexRowSelected > -1 and self.comboBox_ISIN.currentIndex() > -1:
        if self.indexRowSelected > -1:
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

                self.tb_nombre.setText("")
                self.tb_prix.setText("")
                self.update_modelContenir()
                self.update_calendar()
                if model.rowCount() > 0:
                    self.tableView.selectRow(0)
                else:
                    self.tableView.selectRow(-1)

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

    def Isin_changed(self):
        if self.comboBox_ISIN.currentIndex() > -1 or self.indexRowSelected > -1:
            trouve = False
            i = 0
            struct = False

            if self.comboBox_ISIN.currentIndex() > -1:
                isin = self.comboBox_ISIN.currentText()
                # On vérifie le type de l'obligation
                query = QtSql.QSqlQuery()
                query.exec("SELECT noType FROM Obligation WHERE ISIN = '" + isin + "'")
                if query.next():
                    notype = int(query.value(0))
                query.clear()
                if notype == 2:  # Structuré
                    struct = True
            else:   # dans tableau (mais pas dans liste ISIN)
                isin = str(self.modelContenir.record(self.indexRowSelected).value("ISIN"))

            model = self.modelContenir
            while i < model.rowCount() and trouve is False:
                if str(model.record(i).value("ISIN")) == isin:
                    if struct:
                        self.tb_nombre.setText("")
                        self.tb_prix.setText("")
                        self.tb_valo.setText(str(model.record(i).value("Valorisation")))
                        self.tb_valoAcqui.setText(str(model.record(i).value("ValorisationAC")))
                        self.tb_valo.setEnabled(True)
                        self.tb_valoAcqui.setEnabled(True)
                        self.tb_valo_changed()
                        self.tb_valoAcqui_changed()
                        self.tb_nombre.setStyleSheet("")
                        self.tb_prix.setStyleSheet("")
                        self.tb_nombre.setEnabled(False)
                        self.tb_prix.setEnabled(False)
                    else:
                        self.tb_valo.setText("")
                        self.tb_valoAcqui.setText("")
                        self.tb_nombre.setText(str(model.record(i).value("nombre")))
                        self.tb_prix.setText(str(model.record(i).value("prixAchat")))
                        self.tb_valo.setStyleSheet("")
                        self.tb_valoAcqui.setStyleSheet("")
                        self.tb_valo.setEnabled(False)
                        self.tb_valoAcqui.setEnabled(False)
                        self.tb_nombre.setEnabled(True)
                        self.tb_prix.setEnabled(True)
                        self.tb_nombre_changed()
                        self.tb_prix_changed()
                    self.tableView.selectRow(i)
                    trouve = True
                    self.btn_modif.setEnabled(True)
                    self.btn_suppr.setEnabled(True)
                i += 1

            if trouve is False:
                self.tableView.clearSelection()
                if struct:
                    self.tb_valo.setEnabled(True)
                    self.tb_valoAcqui.setEnabled(True)
                    self.tb_valo_changed()
                    self.tb_valoAcqui_changed()
                    self.tb_nombre.setStyleSheet("")
                    self.tb_prix.setStyleSheet("")
                    self.tb_nombre.setEnabled(False)
                    self.tb_prix.setEnabled(False)
                else:
                    self.tb_valo.setStyleSheet("")
                    self.tb_valoAcqui.setStyleSheet("")
                    self.tb_valo.setEnabled(False)
                    self.tb_valoAcqui.setEnabled(False)
                    self.tb_nombre.setEnabled(True)
                    self.tb_prix.setEnabled(True)
                    self.tb_nombre_changed()
                    self.tb_prix_changed()

            query = QtSql.QSqlQuery()
            query.exec("SELECT Nominal, DateDeMAJ, Libelle FROM Obligation WHERE ISIN = '" + isin + "' ORDER BY DateDeMAJ DESC")
            if query.next():
                self.label_nominal.setText(str(query.value(0)))
                self.label_dateMAJ.setText(query.value(1).toString("dd/MM/yyyy"))
                self.label_libelle.setText(str(query.value(2)))
            else:
                self.label_nominal.setText("ISIN inconnu")
                self.label_dateMAJ.setText("ISIN inconnu")
                self.label_libelle.setText("ISIN inconnu")
            query.clear()
        else:
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
