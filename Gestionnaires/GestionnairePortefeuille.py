import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtSql
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QDialogButtonBox, QWidget
from PyQt5.QtGui import QPalette
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
            value = '{'+'{:0>2d}}} {}'.format(noClient, nomEntreprise) 
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
            value = '{'+'{:0>3d}}} {}'.format(noPortefeuille, nomPortefeuille) 
            return value
        return super().data(index, role)


class ModelContenir(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Contenir')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()

    def data(self, index, role=Qt.DisplayRole):

        # Affichage date
        date_column = self.fieldIndex('DateDeMAJ')    
        if role == Qt.DisplayRole and index.column() == date_column:
            date = super().data(index, Qt.EditRole)
            value = date.toString("dd/MM/yyyy")
            return value

        return super().data(index, role)


class ModelISIN(QtSql.QSqlQueryModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setQuery("SELECT DISTINCT ISIN, Libelle FROM Obligation ORDER BY ISIN ASC");



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
        self.calendarWidget.selectionChanged.connect(self.change_date)
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


        # # Mapping table
        # self.mapper = QtWidgets.QDataWidgetMapper(self)
        # self.mapper.setModel(self.modelContenir)
        # self.mapper.addMapping(self.comboBox_ISIN, self.modelContenir.fieldIndex('ISIN'))
        # self.mapper.addMapping(self.tb_nombre, self.modelContenir.fieldIndex('nombre'))
        # self.mapper.addMapping(self.tb_prix, self.modelContenir.fieldIndex('prixAchat'))

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

        self.tb_nombre.textEdited.connect(self.tb_nombre_changed)
        self.tb_nombre_etat = True
        self.tb_prix.textEdited.connect(self.tb_prix_changed)
        self.tb_prix_etat = True

        self.color_error = "#FFCCCC"
        self.color_ok = "#CCE5FF"






    def client_choose(self):
        if self.comboBox_clients.currentIndex() >= 0:
            model = self.modelClient
            index = self.comboBox_clients.currentIndex()
            ID = model.index(index, model.fieldIndex('noClient')).data(Qt.EditRole)
            print('noClient = ',str(ID))
            
            self.clientChoisi.noClient = ID
            self.clientChoisi.get_values()
            
            self.btn_newPortefeuille.setEnabled(True)
            
            self.btn_unlockClient.setEnabled(True)
            self.btn_chooseClient.setEnabled(False)
            self.comboBox_clients.setEnabled(False)

            self.modelPortefeuille.setFilter('noClient = '+str(self.clientChoisi.noClient))
            
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
        self.btn_newPortefeuille.setEnabled(False)
        self.action_deletePortefeuille.setEnabled(False)
        self.label_portefeuilleChoisi.setText('Portefeuille choisi : ')
        #
        #
        self.btn_search.setEnabled(False)
        self.comboBox_ISIN.setEnabled(False)
        self.tb_nombre.setEnabled(False)
        self.tb_prix.setEnabled(False)
        self.btn_modif.setEnabled(False)
        self.btn_suppr.setEnabled(False)
        self.btn_add.setEnabled(False)
        self.btn_import.setEnabled(False)
        self.btn_export.setEnabled(False)

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
            print('noPortefeuille = ',str(noPortefeuille))
            self.portefeuilleChoisi.noPortefeuille = noPortefeuille    
            self.portefeuilleChoisi.get_values()
            self.label_portefeuilleChoisi.setText('Portefeuille choisi : '+model.index(index, model.fieldIndex('noPortefeuille')).data())

            # Dates de mise à jour
            query = QtSql.QSqlQuery()
            query.exec("SELECT DISTINCT DateDeMAJ FROM Contenir WHERE noPortefeuille = " + str(noPortefeuille) + " ORDER BY DateDeMAJ ASC")
            datemax = QDate.currentDate()
            while query.next():
                datemax = query.value(0).date()
                self.calendarWidget.highlight.append(datemax)
            query.clear()

            self.calendarWidget.setSelectedDate(datemax)

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

            ### Affichage liquidité

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
        self.calendarWidget.setEnabled(False)
        self.calendarWidget.highlight = []

        self.btn_choosePortefeuille.setEnabled(True)
        self.portefeuilleChoisi = Portefeuille()

        self.label_portefeuilleChoisi.setText('Portefeuille choisi : ')
        self.update_modelContenir()     
         

    def change_date(self):
        self.dateChoisie = self.calendarWidget.selectedDate()
        print('Date : '+ self.dateChoisie.toString("dd/MM/yyyy"))
        self.tb_dateChoisie.setText(self.dateChoisie.toString("dd/MM/yyyy"))

        self.update_modelContenir()
        

    def update_modelContenir(self):
        # self.modelContenir.setFilter('noPortefeuille = {}'.format(self.portefeuilleChoisi.noPortefeuille))
        self.modelContenir.setFilter('noPortefeuille = {} AND DateDeMAJ = #{}#'.format(self.portefeuilleChoisi.noPortefeuille, self.dateChoisie.toString("MM/dd/yyyy")))
        self.modelContenir.select()

    
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
        print('indexRowSelected = ',str(self.indexRowSelected))
        self.btn_modif.setEnabled(True)
        self.btn_suppr.setEnabled(True)
        self.btn_add.setEnabled(False)

        model = self.modelContenir
        Isin = model.index(index.row(), model.fieldIndex('ISIN')).data()
        print(Isin)
        self.comboBox_ISIN.setCurrentText(Isin)


        
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
                    dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)                
                else:
                    dialog.tb_message.setText("Un portefeuille porte déjà ce nom.")
                    dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            else:
                dialog.tb_message.setText("Format incorrect.")
                dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        dialog = WindowAddPortefeuille(self)
        dialog.tb_client.setText(self.clientChoisi.nomEntreprise)
        dialog.tb_message.setText("Définir un libellé.")
        dialog.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        dialog.tb_libelle.textEdited.connect(textchanged)   


        if dialog.exec() == QtWidgets.QDialog.Accepted :                
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
                'noClient' : self.clientChoisi.noClient,
                'nomPortefeuille' : nom_portefeuille
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
                QMessageBox.information(self, "Nouveau portefeuille", "Ajout réussi")
            else:
                error = model.lastError().text()
                QMessageBox.critical(self, "Database returned an error", error)

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
            query.clear()
            if resul:
                QMessageBox.information(self, "Modification portefeuille", "Modification réussie")
            else:
                QMessageBox.critical(self, "Modification portefeuille", "Modification non réussie")

            self.portefeuilleChoisi.get_values()
            self.label_portefeuilleChoisi.setText("Portefeuille choisie : " + self.portefeuilleChoisi.nomPortefeuille)
            index = self.comboBox_portefeuilles.currentIndex()
            self.modelPortefeuille.select()
            self.comboBox_portefeuilles.setCurrentIndex(index)
        
        else:
            QMessageBox.information(self, "Modification portefeuille", "Modification annulée")


    def delete_portefeuille(self):
        buttonReply = QMessageBox.warning(self, 'Suppression', "Êtes vous sûr de vouloir supprimez ce portefeuille?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if buttonReply == QMessageBox.Yes:
            query = QtSql.QSqlQuery()                
            resul1 = query.exec("DELETE FROM Contenir WHERE noPortefeuille = " + str(self.portefeuilleChoisi.noPortefeuille))
            resul2 = query.exec("DELETE FROM Portefeuille WHERE noPortefeuille = " + str(self.portefeuilleChoisi.noPortefeuille))
            query.clear()
            if resul1 and resul2:
                QMessageBox.information(self, "Suppresion", "Suppression réussie")
            else:
                QMessageBox.critical(self, "Suppresion", "Suppression non réussie")
            
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
        if self.comboBox_ISIN.currentIndex() > -1 and self.tb_nombre_etat and self.tb_prix_etat :  #### A MODIFIER

            model = self.modelContenir
            new_row = model.record()

            if self.tb_nombre.isEnabled:
                nbOrValo = self.tb_nombre.text
                prixOrValoAC = self.tb_prix.text
            else:
                nbOrValo = self.tb_valo.text
                prixOrValoAC = self.tb_valoAcqui.text

            noPort = self.portefeuilleChoisi.noPortefeuille
            Isin = self.comboBox_ISIN.currentText

            defaults = {
                'noPortefeuille': noPort,
                'ISIN' : Isin,
                'DateDeMAJ' : self.dateChoisie.toString("MM/dd/yyyy")
            }

            if self.tb_prix.isEnabled :
                defaults['Nombre'] = self.tb_nombre.text
                defaults['PrixAchat'] = self.tb_prix.text
            else:
                defaults['Valorisation'] = self.tb_valo.text
                defaults['ValorisationAC'] = self.tb_valoAcqui.text


            for field, value in defaults.items():
                index = model.fieldIndex(field)
                new_row .setValue(index, value)

            inserted = model.insertRecord(-1, new_row)
            if not inserted:
                error = model.lastError().text()
                print(f"Insert Failed: {error}")
                model.select()

            if model.submitAll():
                QMessageBox.information(self, "Nouveau portefeuille", "Ajout réussi")
            else:
                error = model.lastError().text()
                QMessageBox.critical(self, "Database returned an error", error)

            self.RajoutObligDateFutur(Isin, noPort, nbOrValo, prixOrValoAC)

            self.modelContenir.select()

        else:
            QMessageBox.information(self, "Ajout", "Ajout impossible: remplir le formulaire")

    
    def RajoutObligDateFutur(self, Isin, noPort, nbOrValo, prixOrValoAC):

        # On va ajouter dans les jours suivants l'Obligation pour chaque date de valorisation
        listDate = []
        query = QtSql.QSqlQuery()
        query.exec("SELECT DISTINCT DateDeMAJ FROM Contenir WHERE noPortefeuille = " + noPort + " AND DateDeMAJ > #" + self.dateChoisie.toString("MM/dd/yyyy") + "#")
        while query.next():
            listDate.append(query.value(0).date())
        query.clear()

        for date in listDate:
            query = QtSql.QSqlQuery()
            query.exec("SELECT count(*) FROM Contenir WHERE noPortefeuille = " + noPort + " AND DateDeMAJ = #" + self.date.toString("MM/dd/yyyy") + "# AND ISIN = '" + Isin + "'")
            if query.next():
                count = int(query.value(0))
            query.clear()

            # On vérifie si elle existe déjà, si oui on l'update (1)
            if count == 1 :
                if self.tb_nombre.isEnabled : # Si c'est pas une structure
                    query = QtSql.QSqlQuery()                
                    resul = query.exec("UPDATE Contenir SET nombre = '" + nbOrValo + "', prixAchat = '" + prixOrValoAC + "' WHERE noPortefeuille = " + noPort + " AND DateDeMAJ = #" + date.toString("MM/dd/yyyy") + "# AND ISIN = '" + Isin + "'")
                    query.clear()
                    if resul:
                        QMessageBox.information(self, "Date future", "Mise à jour à la date future : " + date.toString("dd/MM/yyyy"))
                    else:
                        QMessageBox.critical(self, "Date future", "Mise à jour non réussie")                
                else:
                    query = QtSql.QSqlQuery()                
                    resul = query.exec("UPDATE Contenir SET Valorisation = '" + nbOrValo + "', ValorisationAC = '" + prixOrValoAC + "' WHERE noPortefeuille = " + noPort + " AND DateDeMAJ = #" + date.toString("MM/dd/yyyy") + "# AND ISIN = '" + Isin + "'")
                    query.clear()
                    if resul:
                        QMessageBox.information(self, "Date future", "Mise à jour à la date future : " + date.toString("dd/MM/yyyy"))
                    else:
                        QMessageBox.critical(self, "Date future", "Mise à jour non réussie")                
            else:
                if self.tb_nombre.isEnabled : # Si c'est pas une structure
                    query = QtSql.QSqlQuery()                
                    resul = query.exec("INSERT INTO Contenir (noPortefeuille, ISIN, DateDeMAJ, nombre, prixAchat) VALUES (" + noPort + ",'" + Isin + "',#" + date.toString("MM/dd/yyyy") + "#, '" + nbOrValo + "','" + prixOrValoAC + "')")
                    query.clear()
                    if resul:
                        QMessageBox.information(self, "Date future", "Ajout à la date future : " + date.toString("dd/MM/yyyy"))
                    else:
                        QMessageBox.critical(self, "Date future", "Ajout non réussi")                
                else:
                    query = QtSql.QSqlQuery()                
                    resul = query.exec("INSERT INTO Contenir (noPortefeuille, ISIN, DateDeMAJ, Valorisation, ValorisationAC) VALUES (" + noPort + ",'" + Isin + "',#" + date.toString("MM/dd/yyyy") + "#, '" + nbOrValo + "','" + prixOrValoAC + "')")
                    query.clear()
                    if resul:
                        QMessageBox.information(self, "Date future", "Ajout à la date future : " + date.toString("dd/MM/yyyy"))
                    else:
                        QMessageBox.critical(self, "Date future", "Ajout non réussi") 

    def tb_nombre_changed(self):
        try:
            float(self.tb_nombre.text().replace(",", "."))
            test = True
        except:
            test = False
        
        if test:
            self.tb_nombre.setStyleSheet("background : " + self.color_ok)
            self.tb_nombre_etat = True
        else:
            self.tb_nombre.setStyleSheet("background : " + self.color_error)
            self.tb_nombre_etat = False
            self.btn_modif.setEnabled(False)        
        self.verif()

    def tb_prix_changed(self):
        try:
            float(self.tb_prix.text().replace(",", "."))
            test = True
        except:
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
                self.btn_suppr.setEnabled(True)
            else:
                self.btn_add.setEnabled(True)
        else:
            self.btn_modif.setEnabled(False)
            self.btn_suppr.setEnabled(False)
            self.btn_add.setEnabled(False)

