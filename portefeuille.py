import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtSql
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from database import createconnection


# qt_creator_file = "portefeuille.ui"
# Ui_MainWindowPortefeuille, QtBaseClass = uic.loadUiType(qt_creator_file)
import PortefeuilleUI
from PortefeuilleUI import Ui_MainWindowPortefeuille


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
            noClient = super().data(index, 0)
            nomEntreprise = super().data(self.index(index.row(), nomEntreprise_column), 0)
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
            noPortefeuille = super().data(index, 0)
            nomPortefeuille = super().data(self.index(index.row(), nomPortefeuille_column), 0)
            value = '{'+'{:0>3d}}} {}'.format(noPortefeuille, nomPortefeuille) 
            return value
        return super().data(index, role)




class ModelContenir(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Contenir')
        self.select()

    def data(self, index, role=Qt.DisplayRole):

        # Affichage date
        date_column = self.fieldIndex('DateDeMAJ')    
        if role == Qt.DisplayRole and index.column() == date_column:
            date = super().data(index, 2)
            value = date.toString("dd/MM/yyyy")
            return value

        return super().data(index, role)


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
        self.tableView.selectionModel().selectionChanged.connect(self.change_mapper_index)


        # Liste des clients
        self.modelClient = ModelClient()
        self.noClient = None
        
        self.comboBox_clients.setModel(self.modelClient)
        self.comboBox_clients.setModelColumn(self.modelClient.fieldIndex('noClient'))
        self.comboBox_clients.setCurrentIndex(-1)
        
        self.btn_chooseClient.clicked.connect(self.client_choose)
        self.btn_unlockClient.clicked.connect(self.client_unlock)
        self.btn_unlockClient.setEnabled(False)


        # Liste des portefeuilles
        self.modelPortefeuille = ModelPortefeuille()
        self.noPortefeuille = None

        self.comboBox_portefeuilles.setModel(self.modelPortefeuille)
        self.comboBox_portefeuilles.setCurrentIndex(-1)
        self.comboBox_portefeuilles.setEnabled(False)

        self.btn_choosePortefeuille.clicked.connect(self.portefeuille_choose)
        self.btn_choosePortefeuille.setEnabled(False)        

        self.btn_unlockPortefeuille.clicked.connect(self.portefeuille_unlock)
        self.btn_unlockPortefeuille.setEnabled(False)


        # Calendrier
        self.date = self.calendarWidget.selectedDate()
        self.calendarWidget.selectionChanged.connect(self.change_date)


        # Table vide
        self.update_modelContenir()

        # Nouveau portefeuille
        self.btn_newPortefeuille.setEnabled(False)
        self.btn_newPortefeuille.clicked.connect(self.new_portefeuille)


        # Mapping table
        self.mapper = QtWidgets.QDataWidgetMapper(self)
        self.mapper.setModel(self.modelContenir)
        self.mapper.addMapping(self.comboBox_ISIN, self.modelContenir.fieldIndex('ISIN'))
        self.mapper.addMapping(self.tb_nombre, self.modelContenir.fieldIndex('nombre'))
        self.mapper.addMapping(self.tb_prix, self.modelContenir.fieldIndex('prixAchat'))


    def client_choose(self):
        if self.comboBox_clients.currentIndex() >= 0:
            model = self.modelClient
            index = self.comboBox_clients.currentIndex()
            ID = model.index(index, model.fieldIndex('noClient')).data(2)
            print('noClient = ',str(ID))
            self.noClient = ID
            
            self.btn_newPortefeuille.setEnabled(True)
            
            self.btn_unlockClient.setEnabled(True)
            self.btn_chooseClient.setEnabled(False)
            self.comboBox_clients.setEnabled(False)

            self.modelPortefeuille.setFilter('noClient = '+str(self.noClient))
            
            if self.modelPortefeuille.columnCount() > 0:
                self.btn_choosePortefeuille.setEnabled(True)
                self.comboBox_portefeuilles.setEnabled(True)
            else:
                self.btn_choosePortefeuille.setEnabled(False)
                self.comboBox_portefeuilles.setEnabled(False)
                QMessageBox.warning(None, '', "Aucun portefeuille créé pour le client choisi.")
         
        else:
            QMessageBox.warning(None, '', 'Veuillez choisir un client.')
               
    def client_unlock(self):
        self.btn_unlockClient.setEnabled(False)
        self.btn_chooseClient.setEnabled(True)
        self.comboBox_clients.setEnabled(True)
        self.btn_choosePortefeuille.setEnabled(False)
        self.comboBox_portefeuilles.setEnabled(False)
        #
        self.btn_newPortefeuille.setEnabled(False)
        self.action_deletePortefeuille.setEnable(False)
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


    def portefeuille_choose(self):
        if self.comboBox_portefeuilles.currentIndex() >= 0:
            self.calendarWidget.setSelectedDate(QDate.currentDate())
            
            self.calendarWidget.setEnabled(True)
            self.action_deletePortefeuille.setEnabled(True)
            self.btn_import.setEnabled(True)

            model = self.modelPortefeuille
            index = self.comboBox_portefeuilles.currentIndex()
            noPortefeuille = model.index(index, model.fieldIndex('noPortefeuille')).data(2)
            print('noPortefeuille = ',str(noPortefeuille))
            self.noPortefeuille = noPortefeuille    
            self.label_portefeuilleChoisi.setText('Portefeuille choisi : '+model.index(index, model.fieldIndex('noPortefeuille')).data())

            # Dates de mise à jour
            query = QtSql.QSqlQuery()
            query.exec("SELECT DISTINCT DateDeMAJ FROM Contenir WHERE noPortefeuille = " + str(self.noPortefeuille) + " ORDER BY DateDeMAJ ASC")
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
            QMessageBox.warning(None, '', 'Veuillez choisir un portefeuille.')
  

    def portefeuille_unlock(self):
        self.btn_unlockClient.setEnabled(False)
        self.comboBox_portefeuilles.setEnabled(True)
        self.btn_choosePortefeuille.setEnabled(True)

         

    def change_date(self):
        self.date = self.calendarWidget.selectedDate()
        print('Date : '+ self.date.toString("dd/MM/yyyy"))

        self.update_modelContenir()
        self.tb_dateChoisie.setText(self.date.toString("dd/MM/yyyy"))
        

    def update_modelContenir(self):
        self.modelContenir.setFilter('noPortefeuille = {} AND DateDeMAJ = #{}#'.format(self.noPortefeuille, self.date.toString("dd/MM/yyyy")))
        self.modelContenir.select()

    
    def change_mapper_index(self):
        select = self.tableView.selectionModel()
        if select.hasSelection():
            index = select.selectedRows()[0]
            self.mapper.setCurrentModelIndex(index)

        
    def new_portefeuille(self):
        if not self.noClient:
            QMessageBox.warning(None, 'Nouveau portefeuille', 'Veuillez choisir un client.')
        
        else:
            nom_portefeuille, ok = QInputDialog().getText(None, 'Nouveau protefeuille', 'Client : \nNom du nouveau portefeuille')
            if ok:
                if not nom_portefeuille:
                    QMessageBox.warning(None, 'Nouveau portefeuille', 'Veuillez définir un nom de portefeuille.')
                else:
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
                        'noClient' : self.noClient,
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


def main():
    app = QtWidgets.QApplication(sys.argv)
    createconnection()
    window = MainWindowPortefeuille()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()