<<<<<<< HEAD
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


=======
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import Qt

from Gestionnaires.GestionnaireObligataireUI import Ui_MainWindowObligation


<<<<<<<< HEAD:Gestionnaires/GestionnaireObligataire.py
class ModelObligation(QtSql.QSqlTableModel):
========
>>>>>>> 52fc14adb2c1de3da3a34b0fa002c71ea026afce
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

<<<<<<< HEAD
class ModelObligation(QtSql.QSqlTableModel):
=======
class ModelObligation(QtSql.QSqlTableModel): #TODO à refaire
>>>>>>>> 52fc14adb2c1de3da3a34b0fa002c71ea026afce:GestionnaireObligataire.py
>>>>>>> 52fc14adb2c1de3da3a34b0fa002c71ea026afce
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Obligation')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()

    def data(self, index, role=Qt.DisplayRole):

<<<<<<< HEAD
            # Affichage obligation
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
=======
<<<<<<<< HEAD:Gestionnaires/GestionnaireObligataire.py
        # Affichage noClient
========
        # Affichage obligation
>>>>>>>> 52fc14adb2c1de3da3a34b0fa002c71ea026afce:GestionnaireObligataire.py
        ISIN_column = self.fieldIndex('ISIN')
        libelle_column = self.fieldIndex('libelle')
        if role == Qt.DisplayRole and index.column() == ISIN_column:
            ISIN = super().data(index, 0)
            libelle = super().data(self.index(index.row(), libelle_column), 0)
<<<<<<<< HEAD:Gestionnaires/GestionnaireObligataire.py
            value = '{' + '{:0>2d}}} {}'.format(ISIN, libelle)
            return value
        return super().data(index, role)

========
            value = '{} {}'.format(ISIN, libelle)
            return value
        return super().data(index, role)
>>>>>>>> 52fc14adb2c1de3da3a34b0fa002c71ea026afce:GestionnaireObligataire.py

class MainWindowObligation(QtWidgets.QMainWindow, Ui_MainWindowObligation):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        Ui_MainWindowObligation.__init__(self)
        self.setupUi(self)

>>>>>>> 52fc14adb2c1de3da3a34b0fa002c71ea026afce
        self.modelObligation = ModelObligation()
        self.modelObligation.select()

        self.comboBox_ListeOblig.setModel(self.modelObligation)
        self.comboBox_ListeOblig.setModelColumn(self.modelObligation.fieldIndex('libelle'))
        self.comboBox_ListeOblig.setCurrentIndex(-1)
        self.comboBox_ListeOblig.activated.connect(self.rempli_ligne)
        self.pushButton_Valider.clicked.connect(self.mod_oblig)

<<<<<<< HEAD

=======
>>>>>>> 52fc14adb2c1de3da3a34b0fa002c71ea026afce
    def rempli_ligne(self):
        date = self.calendarWidget.selectedDate()
        datestr = date.toString()
        model = self.modelObligation()
        obli_choisi = "'" + self.comboBox_ListeOblig.currentText() + "'"
        query = QtSql.QSqlQuery()
        query.exec("SELECT ISIN,Ticker,TauxRemb, Nominal, noType, Cours, Coupon, DeviseAchat, DeviseConversion, Maturite, noRegion, noSousSecteur, Libelle, Rendement, Duration, SpreadBund, Sensibilite, Convexite, VieMoyenne, Indexation, Rating, RatingSP, RatingFITCH, RatingMOODY  FROM obligation WHERE libelle = " + obli_choisi + " AND DateDeMaj = " + datestr)
<<<<<<< HEAD
        #TODO : rajouter classe duration/interets courus
=======
        # TODO : rajouter classe duration/interets courus
>>>>>>> 52fc14adb2c1de3da3a34b0fa002c71ea026afce
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
            avglife=  query.value(18)
            indexation =  query.value(19)
            rating =  query.value(20)
            ratingsp =  query.value(21)
            ratingfitch =  query.value(22)
            ratingmoody =  query.value(23)
        else:
            error = model.lastError().text()
            print(f"Insert Failed: {error}")
            model.select()

        self.lineEdit_ISIN.setText(str(isin))
        self.lineEdit_Nominal.setText(str(nominal))
        self.lineEdit_Cours.setText(str(cours))
        self.lineEdit_Coupon.setText(str(coupon))
        self.lineEdit_DevisePassee.setText(str(deviseachat))
        self.lineEdit_DevisePrst.setText(str(deviseconversion))
        self.lineEdit_Libelle.setText(str(libelle2))
        self.lineEdit_Rendement.setText(str(rendement))
        #TODO rajouter duration
        self.lineEdit_SpreadBund.setText(str(spreadbund))
<<<<<<< HEAD
=======
<<<<<<<< HEAD:Gestionnaires/GestionnaireObligataire.py
# TODO une première fonction qui se lance au signal de la combo box -> rempli les line edit
# TODO une deuxieme fonction qui se lance au signal du bouton valider -> change la base access
========
>>>>>>> 52fc14adb2c1de3da3a34b0fa002c71ea026afce
        #TODO rajouter interets courus
        self.lineEdit_Sensibilite.setText(str(sensibilite))
        self.lineEdit_Convexite.setText(str(convexite))
        self.lineEdit_AvgLife.setText(str(avglife))
        self.lineEdit_Indexation.setText(str(indexation))
#TODO une première fonction qui se lance au signal de la combo box -> rempli les line edit
#TODO une deuxieme fonction qui se lance au signal du bouton valider -> change la base access
    def mod_oblig(self):
        date = self.calendarWidget.selectedDate()

        modISIN = self.lineEdit_ISIN.text()
        modNominal = self.lineEdit_Nominal.text()
        modCours = self.lineEdit_Cours.text()
        modCoupon = self.lineEdit_Coupon.text()
        modDevisePassee = self.lineEdit_DevisePassee.text()
        modDevisePrst = self.lineEdit_DevisePrst.text()
        modLibelle = self.lineEdit_Libelle.text()
        modRendement = self.lineEdit_Rendement.text()
        #TODO rajouter duration
        modSpreadBund = self.lineEdit_SpreadBund.text()
        #TODO rajouter interets courus
        modSensibilite = self.lineEdit_Sensibilite.text()
        modConvexite = self.lineEdit_Convexite.text()
        modAvgLife = self.lineEdit_AvgLife.text()
        modIndexation = self.lineEdit_Indexation.text()

        query = QtSql.QSqlQuery()
        result = query2.exec("UPDATE Obligation SET ISIN = '" + modISIN +"', Libelle = '" + modLibelle +"', Nominal = '"+ modNominal +"', Cours = '"+ modCours +"'Coupon = '" + modCoupon +"', Libelle = '" + modLibelle +"', Rendement = '"+ modRendement +"', SpreadBund = '"+ modSpreadBund +"'Sensibilite = '" + modSensibilite +"', Convexite = '"+ modConvexite +"'VieMoyenne = '" + modAvgLife+"' Indexation = '"+modIndexation+"'DeviseAchat = '"+ modDevisePassee+"' DeviseConversion = '"+ modDevisePrst+"' WHERE ISIN = '" + modISIN +"' OR DateMaj ='" + str(date))
        #TODO rajouter classe duration et interets courus
        if query:
            QMessageBox.information(self, "Client Modifié", "Modification Reussie")
            self.lineEdit_ISIN.clear()
            self.lineEdit_Nominal.clear()
            self.lineEdit_Cours.clear()
            self.lineEdit_Coupon.clear()
            self.lineEdit_DevisePassee.clear()
            self.lineEdit_DevisePrst.clear()
            self.lineEdit_Libelle.clear()
            self.lineEdit_Rendement.setText(str(rendement))
            #TODO rajouter duration
            self.lineEdit_SpreadBund.setText(str(spreadbund))
            #TODO rajouter interets courus
            self.lineEdit_Sensibilite.setText(str(sensibilite))
            self.lineEdit_Convexite.setText(str(convexite))
            self.lineEdit_AvgLife.setText(str(avglife))
            self.lineEdit_Indexation.setText(str(indexation))
        else:
            error = model.lastError().text()
            print("erreur")
            QMessageBox.critical(self, "erreur 1", error)
app = QtWidgets.QApplication(sys.argv)
window = MainWindowObligation()
window.show()
app.exec_()
<<<<<<< HEAD
window.show
=======
window.show
>>>>>>>> 52fc14adb2c1de3da3a34b0fa002c71ea026afce:GestionnaireObligataire.py
>>>>>>> 52fc14adb2c1de3da3a34b0fa002c71ea026afce
