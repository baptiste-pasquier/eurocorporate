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
import GestionnaireObligataireUI
from GestionnaireObligataireUI import Ui_MainWindowObligation


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

class ModelObligation(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Obligation')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()

    def data(self, index, role=Qt.DisplayRole):

            # Affichage noClient
            ISIN_column = self.fieldIndex('ISIN')
            libelle_column = self.fieldIndex('libelle')
            if role == Qt.DisplayRole and index.column() == ISIN_column:
                ISIN = super().data(index, 0)
                libelle = super().data(self.index(index.row(), libelle_column), 0)
                value = '{'+'{:0>2d}}} {}'.format(ISIN, libelle)
                return value
            return super().data(index, role)

class MainWindowObligation(QtWidgets.QMainWindow, Ui_MainWindowObligation):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindowObligation.__init__(self)
        self.setupUi(self)

        self.db = createconnection()
        self.modelObligation = ModelObligation()
        self.modelObligation.select()

        self.comboBox_ListeOblig.setModel(self.modelObligation)
        self.comboBox_ListeOblig.setModelColumn(self.modelObligation.fieldIndex('libelle'))
        self.comboBox_ListeOblig.setCurrentIndex(-1)
        self.comboBox_ListeOblig.activated.connect(self.rempli_ligne())


    def rempli_ligne(self):
        date = self.calendarWidget.selectedDate()
        datestr = date.toString()
        model = self.modelObligation()
        obli_choisi = "'" + self.comboBox_ListeOblig.currentText() + "'"
        query = QtSql.QSqlQuery()
        query.exec("SELECT ISIN,Ticker,TauxRemb, Nominal, noType, Cours, Coupon, DeviseAchat, DeviseConversion, Maturite, noRegion, noSousSecteur, Libelle, Rendement, Duration, SpreadBund, Sensibilite, Convexite, VieMoyenne, Indexation, Rating, RatingSP, RatingFITCH, RatingMOODY  FROM obligation WHERE libelle = " + obli_choisi + " AND DateDeMaj = " + datestr)
        #TODO : rajouter classe duration/interets courus
        if query:
            isin = query.value(0)
            ticker = query.value(1)
            tauxremb = query.value(2)
            nominal =  query.value(3)
            notype =  query.value(4)
            cours =  query.value(5)
            coupon =  query.value(6)
            deviseachat =  query.value(7)
            deviseconversion =  query.value(8)
            maturite =  query.value(9)
            noregion =  query.value(10)
            nosoussecteur =  query.value(11)
            libelle2 =  query.value(12)
            rendement =  query.value(13)
            duration =  query.value(14)
            spreadbund =  query.value(15)
            sensibilite =  query.value(16)
            convexite =  query.value(17)
            viemoyenne=  query.value(18)
            indexation =  query.value(19)
            rating =  query.value(20)
            ratingsp =  query.value(21)
            ratingfitch =  query.value(22)
            ratingmoody =  query.value(23)
        else:
            error = model.lastError().text()
            print(f"Insert Failed: {error}")
            model.select()

        self.lineEdit_SpreadBund.setText(str(spreadbund))
#TODO une première fonction qui se lance au signal de la combo box -> rempli les line edit
#TODO une deuxieme fonction qui se lance au signal du bouton valider -> change la base access

app = QtWidgets.QApplication(sys.argv)
window = MainWindowObligation()
window.show()
app.exec_()
window.show