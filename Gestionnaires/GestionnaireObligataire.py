import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5 import QtCore, QtSql, QtWidgets, uic
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import (QDialogButtonBox, QFileDialog, QMessageBox,
                             QProgressDialog)

from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import Qt

from Gestionnaires.GestionnaireObligataireUI import Ui_MainWindowObligation


#Création des Model pour les différentes combo box
class ModelRating(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Rating')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()
    def data(self, index, role=Qt.DisplayRole):
            # Affichage rating
            Rating_column = self.fieldIndex('Rating')
            if role == Qt.DisplayRole and index.column() == Rating_column:
                Rating = super().data(index, 0)
                value = '{}'.format(Rating)
                return value
            return super().data(index, role)

class ModelRatingMoody(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Rating')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()
    def data(self, index, role=Qt.DisplayRole):
            # Affichage rating
            Rating_column = self.fieldIndex('RatingMoody')
            if role == Qt.DisplayRole and index.column() == Rating_column:
                Rating = super().data(index, 0)
                value = '{}'.format(Rating)
                return value
            return super().data(index, role)

class ModelRatingSP(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Rating')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()
    def data(self, index, role=Qt.DisplayRole):
            # Affichage rating
            Rating_column = self.fieldIndex('RatingSP')
            if role == Qt.DisplayRole and index.column() == Rating_column:
                Rating = super().data(index, 0)
                value = '{}'.format(Rating)
                return value
            return super().data(index, role)

class ModelRatingFitch(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Rating')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()
    def data(self, index, role=Qt.DisplayRole):
            # Affichage rating
            Rating_column = self.fieldIndex('RatingFitch')
            if role == Qt.DisplayRole and index.column() == Rating_column:
                Rating = super().data(index, 0)
                value = '{}'.format(Rating)
                return value
            return super().data(index, role)

class ModelTicker(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Emetteur')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()
    def data(self, index, role=Qt.DisplayRole):
            # Affichage Ticker
            Ticker_column = self.fieldIndex('ticker')
            if role == Qt.DisplayRole and index.column() == Ticker_column:
                Ticker = super().data(index, 0)
                value = '{}'.format(Ticker)
                return value
            return super().data(index, role)

class ModelRegion(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Region')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()
    def data(self, index, role=Qt.DisplayRole):
            # Affichage rating
            Region_column = self.fieldIndex('nomRegion')
            if role == Qt.DisplayRole and index.column() == Region_column:
                Region = super().data(index, 0)
                value = '{}'.format(Region)
                return value
            return super().data(index, role)

class ModelType(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('TypeOblig')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()
    def data(self, index, role=Qt.DisplayRole):
            # Affichage rating
            Type_column = self.fieldIndex('nomType')
            if role == Qt.DisplayRole and index.column() == Type_column:
                Type = super().data(index, 0)
                value = '{}'.format(Type)
                return value
            return super().data(index, role)

class ModelDuration(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('ClasseDuration')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()
    def data(self, index, role=Qt.DisplayRole):
            # Affichage rating
            Duration_column = self.fieldIndex('nomClasseDur')
            if role == Qt.DisplayRole and index.column() == Duration_column:
                Duration = super().data(index, 0)
                value = '{}'.format(Duration)
                return value
            return super().data(index, role)

class ModelSSecteur(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('SousSecteur')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()
    def data(self, index, role=Qt.DisplayRole):
            # Affichage rating
            SSecteur_column = self.fieldIndex('nomSousSecteur')
            if role == Qt.DisplayRole and index.column() == SSecteur_column:
                SSecteur = super().data(index, 0)
                value = '{}'.format(SSecteur)
                return value
            return super().data(index, role)

class ModelObligation(QtSql.QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTable('Obligation')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.select()

    def data(self, index, role=Qt.DisplayRole):
            # Affichage obligation
            ISIN_column = self.fieldIndex('ISIN')
            libelle_column = self.fieldIndex('libelle')
            if role == Qt.DisplayRole and index.column() == ISIN_column:
                ISIN = super().data(index, 0)
                libelle = super().data(self.index(index.row(), libelle_column), 0)
                value = '{} {}'.format(ISIN,libelle)
                return value
            return super().data(index, role)

class MainWindowObligation(QtWidgets.QMainWindow, Ui_MainWindowObligation):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        Ui_MainWindowObligation.__init__(self)
        self.setupUi(self)
#Combo box des obligations
        self.modelObligation = ModelObligation()
        self.modelObligation.select()

        self.calendarWidget.clicked.connect(self.prep_combobox)


        self.comboBox_ListeOblig.activated.connect(self.rempli_ligne)


#Combo box des recherches par ticker
        self.lineEdit_SrchTicker.textEdited.connect(self.prep_comboboxSrchTicker)
        self.comboBox_SrchTicker.activated.connect(self.rempli_ligne_srchticker)

#Combo box des recherches par code
        self.lineEdit_SrchCode.textEdited.connect(self.prep_comboboxSrchCode)
        self.comboBox_SrchCode.activated.connect(self.rempli_ligne_srchcode)

        self.pushButton_Valider.clicked.connect(self.mod_oblig)
#ComboBox des Ratings
        self.modelRating = ModelRating()
        self.modelRating.select()

        self.comboBox_Rating.setModel(self.modelRating)
        self.comboBox_Rating.setModelColumn(self.modelRating.fieldIndex('rating'))
        self.comboBox_Rating.setCurrentIndex(-1)

#Combo box des RatingSP
        self.modelRatingSP = ModelRatingSP()
        self.modelRatingSP.select()

        self.comboBox_RatingSP.setModel(self.modelRatingSP)
        self.comboBox_RatingSP.setModelColumn(self.modelRatingSP.fieldIndex('ratingSP'))
        self.comboBox_RatingSP.setCurrentIndex(-1)

#Combo box des RatingMoody
        self.modelRatingMoody = ModelRatingMoody()
        self.modelRatingMoody.select()

        self.comboBox_RatingMoody.setModel(self.modelRatingMoody)
        self.comboBox_RatingMoody.setModelColumn(self.modelRating.fieldIndex('ratingMOODY'))
        self.comboBox_RatingMoody.setCurrentIndex(-1)

#Combo box des RatingFitch
        self.modelRatingFitch = ModelRatingFitch()
        self.modelRatingFitch.select()

        self.comboBox_RatingFitch.setModel(self.modelRatingFitch)
        self.comboBox_RatingFitch.setModelColumn(self.modelRating.fieldIndex('ratingFITCH'))
        self.comboBox_RatingFitch.setCurrentIndex(-1)

#Combo box des Régions
        self.modelRegion = ModelRegion()
        self.modelRegion.select()

        self.comboBox_Region.setModel(self.modelRegion)
        self.comboBox_Region.setModelColumn(self.modelRegion.fieldIndex('nomRegion'))
        self.comboBox_Region.setCurrentIndex(-1)

#Combo box des Tickers
        self.modelTicker = ModelTicker()
        self.modelTicker.select()

        self.comboBox_Ticker.setModel(self.modelTicker)
        self.comboBox_Ticker.setModelColumn(self.modelTicker.fieldIndex('ticker'))
        self.comboBox_Region.setCurrentIndex(-1)

#Combo box des types
        self.modelType = ModelType()
        self.modelType.select()

        self.comboBox_Type.setModel(self.modelType)
        self.comboBox_Type.setModelColumn(self.modelType.fieldIndex('nomtype'))
        self.comboBox_Type.setCurrentIndex(-1)

#Combo box des classe duration
        self.modelDuration = ModelDuration()
        self.modelDuration.select()

        self.comboBox_ClasseDuration.setModel(self.modelDuration)
        self.comboBox_ClasseDuration.setModelColumn(self.modelDuration.fieldIndex('nomClasseDur'))
        self.comboBox_ClasseDuration.setCurrentIndex(-1)

#Combo box des SousSecteur
        self.modelSSecteur = ModelSSecteur()
        self.modelSSecteur.select()

        self.comboBox_SsSecteur.setModel(self.modelSSecteur)
        self.comboBox_SsSecteur.setModelColumn(self.modelSSecteur.fieldIndex('nomSousSecteur'))
        self.comboBox_SsSecteur.setCurrentIndex(-1)

#Action du bouton "nouvelle obligation"

        self.pushBtton_NvlOblig.clicked.connect(self.nvl_oblig)

    def prep_combobox(self):
#Construction de la combo box par une étape de sql
        date1 = self.calendarWidget.selectedDate()
        if len(str(date1.day())) < 2:
            day = "0" + str(date1.day())
        else: day = str(date1.day())

        if len(str(date1.month())) <2:
            month = "0" +str(date1.month())
        else: month = str(date1.month())
        date1str = str(day) + "/" + str(month) + "/" + str(date1.year())


        liste = []
        query_liste = QtSql.QSqlQuery()
        query_liste.exec("SELECT libelle FROM Obligation WHERE DateDeMaj = format('" + date1str + "','dd/mm/yyyy')")

        if query_liste.first():
            liste.append(query_liste.value(0))
            while query_liste.next():
                liste.append(query_liste.value(0))
        else:
            error = self.modelObligation.lastError().text()
            print("erreur 22")
            QMessageBox.critical(self, "Erreur : aucun champ trouvé à cette date", error)

        self.comboBox_ListeOblig.addItems(liste)

    def prep_comboboxSrchCode(self):
#Construction de la combo box par une étape de sql

        isin = self.lineEdit_SrchCode.text()

        date1 = self.calendarWidget.selectedDate()
        if len(str(date1.day())) < 2:
            day = "0" + str(date1.day())
        else: day = str(date1.day())

        if len(str(date1.month())) <2:
            month = "0" +str(date1.month())
        else: month = str(date1.month())
        date1str = str(day) + "/" + str(month) + "/" + str(date1.year())


        liste = []
        query_liste = QtSql.QSqlQuery()
        query_liste.exec("SELECT libelle FROM Obligation WHERE ISIN LIKE '" + isin +"%' AND DateDeMaj = format('" + date1str + "','dd/mm/yyyy')")
        print("SELECT libelle FROM Obligation WHERE ISIN LIKE '" + isin +"%' AND DateDeMaj = format('" + date1str + "','dd/mm/yyyy')")

        if query_liste.first():
            liste.append(query_liste.value(0))
            while query_liste.next():
                liste.append(query_liste.value(0))
        else:
            error = self.modelObligation.lastError().text()
            QMessageBox.critical(self, "Erreur : aucun champ trouvé pour cet  ISIN", error)

        self.comboBox_SrchCode.addItems(liste)


    def prep_comboboxSrchTicker(self):
#Construction de la combo box par une étape de sql

        ticker = self.lineEdit_SrchTicker.text()

        date1 = self.calendarWidget.selectedDate()
        if len(str(date1.day())) < 2:
            day = "0" + str(date1.day())
        else: day = str(date1.day())

        if len(str(date1.month())) <2:
            month = "0" +str(date1.month())
        else: month = str(date1.month())
        date1str = str(day) + "/" + str(month) + "/" + str(date1.year())


        liste = []
        query_liste = QtSql.QSqlQuery()
        query_liste.exec("SELECT libelle FROM Obligation WHERE ticker LIKE '" + ticker +"%' AND DateDeMaj = format('" + date1str + "','dd/mm/yyyy')")

        if query_liste.first():
            liste.append(query_liste.value(0))
            while query_liste.next():
                liste.append(query_liste.value(0))
        else:
            error = self.modelObligation.lastError().text()

            QMessageBox.critical(self, "Erreur : aucun champ trouvé pour ce Ticker", error)

        self.comboBox_SrchTicker.addItems(liste)

    def rempli_ligne(self):
        date = self.calendarWidget.selectedDate()

        if len(str(date.day())) < 2:
            day2 = "0" + str(date.day())
        else: day2 = str(date.day())

        if len(str(date.month())) <2:
            month2 = "0" +str(date.month())
        else: month2 = str(date.month())
        datestr = str(day2) + "/" + str(month2) + "/" + str(date.year())

        model = self.modelObligation
        obli_choisi = "'" + self.comboBox_ListeOblig.currentText() + "'"
        query = QtSql.QSqlQuery()
        query.exec("SELECT ISIN,Ticker,TauxRemb, Nominal, noType, Cours, Coupon, DeviseAchat, DeviseConversion, Maturite, noRegion, noSousSecteur, Libelle, Rendement, Duration, SpreadBund, Sensibilite, Convexite, VieMoyenne, Indexation, Rating, RatingSP, RatingFITCH, RatingMOODY  FROM obligation WHERE libelle = " + obli_choisi + " AND DateDeMaj = " +"format('" + datestr + "','dd/mm/yyyy')")

        if query.next():
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
        self.lineEdit_Duration.setText(str(duration))
        #TODO rajouter classe duration
        self.lineEdit_SpreadBund.setText(str(spreadbund))

        #TODO rajouter interets courus
        self.lineEdit_Sensibilite.setText(str(sensibilite))
        self.lineEdit_Convexite.setText(str(convexite))
        self.lineEdit_AvgLife.setText(str(avglife))
        self.lineEdit_Indexation.setText(str(indexation))

        index_ticker = self.comboBox_Ticker.findText(str(ticker))
        self.comboBox_Ticker.setCurrentIndex(index_ticker)

        index_rating = self.comboBox_Rating.findText(str(rating))
        self.comboBox_Rating.setCurrentIndex(index_rating)

        index_ratingsp = self.comboBox_RatingSP.findText(str(ratingsp))
        self.comboBox_RatingSP.setCurrentIndex(index_ratingsp)

        index_ratingmoody = self.comboBox_RatingMoody.findText(str(ratingmoody))
        self.comboBox_RatingMoody.setCurrentIndex(index_ratingmoody)

        index_ratingfitch = self.comboBox_RatingFitch.findText(str(ratingfitch))
        self.comboBox_RatingFitch.setCurrentIndex(index_ratingfitch)

        index_ratingfitch = self.comboBox_RatingFitch.findText(str(ratingfitch))
        self.comboBox_RatingFitch.setCurrentIndex(index_ratingfitch)

        queryregion = QtSql.QSqlQuery()
        resultregion = queryregion.exec("SELECT nomRegion FROM region WHERE noRegion =" + str(noregion))
        if queryregion.first():
            nomregion = queryregion.value(0)
            index_region = self.comboBox_Region.findText(nomregion)
            self.comboBox_Region.setCurrentIndex(index_region)

        queryssecteur = QtSql.QSqlQuery()
        resultssecteur = queryssecteur.exec("SELECT nomSousSecteur FROM SousSecteur WHERE nosoussecteur = " + str(nosoussecteur))
        if queryssecteur.first():
            nomsoussecteur = queryssecteur.value(0)
            index_ssecteur = self.comboBox_SsSecteur.findText(nomsoussecteur)
            self.comboBox_SsSecteur.setCurrentIndex(index_ssecteur)

        querytype = QtSql.QSqlQuery()
        resulttype = querytype.exec("SELECT nomType FROM TypeOblig WHERE noType = " + str(notype))
        if querytype.first():
            nomtype = querytype.value(0)
            index_type = self.comboBox_Type.findText(nomtype)
            self.comboBox_Type.setCurrentIndex(index_type)

    def rempli_ligne_srchcode(self):
        date = self.calendarWidget.selectedDate()

        if len(str(date.day())) < 2:
            day2 = "0" + str(date.day())
        else: day2 = str(date.day())

        if len(str(date.month())) <2:
            month2 = "0" +str(date.month())
        else: month2 = str(date.month())
        datestr = str(day2) + "/" + str(month2) + "/" + str(date.year())

        model = self.modelObligation
        obli_choisi = "'" + self.comboBox_SrchCode.currentText() + "'"
        query = QtSql.QSqlQuery()
        query.exec("SELECT ISIN,Ticker,TauxRemb, Nominal, noType, Cours, Coupon, DeviseAchat, DeviseConversion, Maturite, noRegion, noSousSecteur, Libelle, Rendement, Duration, SpreadBund, Sensibilite, Convexite, VieMoyenne, Indexation, Rating, RatingSP, RatingFITCH, RatingMOODY  FROM obligation WHERE libelle = " + obli_choisi + " AND DateDeMaj = " +"format('" + datestr + "','dd/mm/yyyy')")

        if query.next():
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
        self.lineEdit_Duration.setText(str(duration))
        #TODO rajouter classe duration
        self.lineEdit_SpreadBund.setText(str(spreadbund))

        #TODO rajouter interets courus
        self.lineEdit_Sensibilite.setText(str(sensibilite))
        self.lineEdit_Convexite.setText(str(convexite))
        self.lineEdit_AvgLife.setText(str(avglife))
        self.lineEdit_Indexation.setText(str(indexation))

        index_ticker = self.comboBox_Ticker.findText(str(ticker))
        self.comboBox_Ticker.setCurrentIndex(index_ticker)

        index_rating = self.comboBox_Rating.findText(str(rating))
        self.comboBox_Rating.setCurrentIndex(index_rating)

        index_ratingsp = self.comboBox_RatingSP.findText(str(ratingsp))
        self.comboBox_RatingSP.setCurrentIndex(index_ratingsp)

        index_ratingmoody = self.comboBox_RatingMoody.findText(str(ratingmoody))
        self.comboBox_RatingMoody.setCurrentIndex(index_ratingmoody)

        index_ratingfitch = self.comboBox_RatingFitch.findText(str(ratingfitch))
        self.comboBox_RatingFitch.setCurrentIndex(index_ratingfitch)

        index_ratingfitch = self.comboBox_RatingFitch.findText(str(ratingfitch))
        self.comboBox_RatingFitch.setCurrentIndex(index_ratingfitch)

        queryregion = QtSql.QSqlQuery()
        resultregion = queryregion.exec("SELECT nomRegion FROM region WHERE noRegion =" + str(noregion))
        if queryregion.first():
            nomregion = queryregion.value(0)
            index_region = self.comboBox_Region.findText(nomregion)
            self.comboBox_Region.setCurrentIndex(index_region)

        queryssecteur = QtSql.QSqlQuery()
        resultssecteur = queryssecteur.exec("SELECT nomSousSecteur FROM SousSecteur WHERE nosoussecteur = " + str(nosoussecteur))
        if queryssecteur.first():
            nomsoussecteur = queryssecteur.value(0)
            index_ssecteur = self.comboBox_SsSecteur.findText(nomsoussecteur)
            self.comboBox_SsSecteur.setCurrentIndex(index_ssecteur)

        querytype = QtSql.QSqlQuery()
        resulttype = querytype.exec("SELECT nomType FROM TypeOblig WHERE noType = " + str(notype))
        if querytype.first():
            nomtype = querytype.value(0)
            index_type = self.comboBox_Type.findText(nomtype)
            self.comboBox_Type.setCurrentIndex(index_type)

    def rempli_ligne_srchticker(self):

        #Fonction de recherche dans la base ACCESS via le TICKER à la date saisie dans le Calendrier
        date = self.calendarWidget.selectedDate()

        if len(str(date.day())) < 2:
            day2 = "0" + str(date.day())
        else: day2 = str(date.day())

        if len(str(date.month())) <2:
            month2 = "0" +str(date.month())
        else: month2 = str(date.month())
        datestr = str(day2) + "/" + str(month2) + "/" + str(date.year())

        model = self.modelObligation
        obli_choisi = "'" + self.comboBox_SrchTicker.currentText() + "'"
        query = QtSql.QSqlQuery()
        query.exec("SELECT ISIN,Ticker,TauxRemb, Nominal, noType, Cours, Coupon, DeviseAchat, DeviseConversion, Maturite, noRegion, noSousSecteur, Libelle, Rendement, Duration, SpreadBund, Sensibilite, Convexite, VieMoyenne, Indexation, Rating, RatingSP, RatingFITCH, RatingMOODY  FROM obligation WHERE libelle = " + obli_choisi + " AND DateDeMaj = " +"format('" + datestr + "','dd/mm/yyyy')")

        if query.next():
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
        self.lineEdit_Duration.setText(str(duration))
        #TODO rajouter classe duration
        self.lineEdit_SpreadBund.setText(str(spreadbund))
        #TODO rajouter interets courus
        self.lineEdit_Sensibilite.setText(str(sensibilite))
        self.lineEdit_Convexite.setText(str(convexite))
        self.lineEdit_AvgLife.setText(str(avglife))
        self.lineEdit_Indexation.setText(str(indexation))

        #Traitement des combo box
        index_ticker = self.comboBox_Ticker.findText(str(ticker))
        self.comboBox_Ticker.setCurrentIndex(index_ticker)

        index_rating = self.comboBox_Rating.findText(str(rating))
        self.comboBox_Rating.setCurrentIndex(index_rating)

        index_ratingsp = self.comboBox_RatingSP.findText(str(ratingsp))
        self.comboBox_RatingSP.setCurrentIndex(index_ratingsp)

        index_ratingmoody = self.comboBox_RatingMoody.findText(str(ratingmoody))
        self.comboBox_RatingMoody.setCurrentIndex(index_ratingmoody)

        index_ratingfitch = self.comboBox_RatingFitch.findText(str(ratingfitch))
        self.comboBox_RatingFitch.setCurrentIndex(index_ratingfitch)

        index_ratingfitch = self.comboBox_RatingFitch.findText(str(ratingfitch))
        self.comboBox_RatingFitch.setCurrentIndex(index_ratingfitch)

        queryregion = QtSql.QSqlQuery()
        resultregion = queryregion.exec("SELECT nomRegion FROM region WHERE noRegion =" + str(noregion))
        if queryregion.first():
            nomregion = queryregion.value(0)
            index_region = self.comboBox_Region.findText(nomregion)
            self.comboBox_Region.setCurrentIndex(index_region)

        queryssecteur = QtSql.QSqlQuery()
        resultssecteur = queryssecteur.exec("SELECT nomSousSecteur FROM SousSecteur WHERE nosoussecteur = " + str(nosoussecteur))
        if queryssecteur.first():
            nomsoussecteur = queryssecteur.value(0)
            index_ssecteur = self.comboBox_SsSecteur.findText(nomsoussecteur)
            self.comboBox_SsSecteur.setCurrentIndex(index_ssecteur)

        querytype = QtSql.QSqlQuery()
        resulttype = querytype.exec("SELECT nomType FROM TypeOblig WHERE noType = " + str(notype))
        if querytype.first():
            nomtype = querytype.value(0)
            index_type = self.comboBox_Type.findText(nomtype)
            self.comboBox_Type.setCurrentIndex(index_type)


    def mod_oblig(self):

        #Modifie la base ACCESS selon les données saisies par l'utilisateur
        model = self.modelObligation
        date = self.calendarWidget.selectedDate()

        if len(str(date.day())) < 2:
            day2 = "0" + str(date.day())
        else: day2 = str(date.day())

        if len(str(date.month())) <2:
            month2 = "0" +str(date.month())
        else: month2 = str(date.month())
        datestr = str(day2) + "/" + str(month2) + "/" + str(date.year())


        modISIN = self.lineEdit_ISIN.text()
        modNominal = self.lineEdit_Nominal.text()
        modCours = self.lineEdit_Cours.text()
        modCoupon = self.lineEdit_Coupon.text()
        modDevisePassee = self.lineEdit_DevisePassee.text()
        modDevisePrst = self.lineEdit_DevisePrst.text()
        modLibelle = self.lineEdit_Libelle.text()
        modRendement = self.lineEdit_Rendement.text()
        modDuration = self.lineEdit_Duration.text()
        #TODO rajouter classe duration
        modSpreadBund = self.lineEdit_SpreadBund.text()
        #TODO rajouter interets courus
        modSensibilite = self.lineEdit_Sensibilite.text()
        modConvexite = self.lineEdit_Convexite.text()
        modAvgLife = self.lineEdit_AvgLife.text()
        modIndexation = self.lineEdit_Indexation.text()

        modTicker = self.comboBox_Ticker.currentText()

        modType = self.comboBox_Type.currentText()
        qType =  QtSql.QSqlQuery()
        rType = qType.exec("SELECT noType FROM TypeOblig WHERE nomType = '" + modType +"'")
        if qType.first():
            smodType = str(qType.value(0))

        modRegion = self.comboBox_Region.currentText()
        qRegion =  QtSql.QSqlQuery()
        rRegion = qRegion.exec("SELECT noRegion FROM Region WHERE nomRegion = '" + str(modRegion) + "'")

        if qRegion.first():
            smodRegion = str(qRegion.value(0))

        modSsecteur = self.comboBox_SsSecteur.currentText()
        qSsecteur =  QtSql.QSqlQuery()
        rSsecteur = qSsecteur.exec("SELECT noSousSecteur FROM SousSecteur WHERE nomSousSecteur = '" + modSsecteur +"'")
        if qSsecteur.first():
            smodSsecteur = str(qSsecteur.value(0))

        modMaturite  = self.comboBox_Maturite.currentText()
        modClasseDuration = self.comboBox_ClasseDuration.currentText() #???

        modRating = self.comboBox_Rating.currentText()
        modRatingSP = self.comboBox_RatingSP.currentText()
        modRatingMoody = self.comboBox_RatingMoody.currentText()
        modRatingFitch = self.comboBox_RatingFitch.currentText()


        query2 = QtSql.QSqlQuery()
        result = query2.exec("UPDATE Obligation SET ISIN = '" + modISIN +"', Libelle = '" + modLibelle +"', Ticker = '"+modTicker +"', noType = "+smodType+" ,Nominal = "+ modNominal +", Cours = "+ modCours +", Coupon = " + modCoupon +", DeviseAchat = "+ modDevisePassee+", DeviseConversion = "+ modDevisePrst+", noRegion = "+ smodRegion +", noSousSecteur = "+ smodSsecteur+", Rendement = "+ modRendement +", SpreadBund = "+ modSpreadBund +", Duration = "+modDuration + ", Sensibilite = " + modSensibilite +", Convexite = "+ modConvexite +", VieMoyenne = " + modAvgLife +", Indexation = '"+ modIndexation +"'  WHERE ISIN = '" + modISIN +"' AND DateDeMaj =  format('" + datestr + "','dd/mm/yyyy')")

        #TODO rajouter classe duration et interets courus
        if result:
            QMessageBox.information(self, "Client Modifié", "Modification Reussie")
            self.lineEdit_ISIN.clear()
            self.lineEdit_Nominal.clear()
            self.lineEdit_Cours.clear()
            self.lineEdit_Coupon.clear()
            self.lineEdit_DevisePassee.clear()
            self.lineEdit_DevisePrst.clear()
            self.lineEdit_Libelle.clear()
            self.lineEdit_Rendement.clear()
            #TODO rajouter duration
            self.lineEdit_SpreadBund.clear()
            #TODO rajouter interets courus
            self.lineEdit_Sensibilite.clear()
            self.lineEdit_Convexite.clear()
            self.lineEdit_AvgLife.clear()
            self.lineEdit_Indexation.clear()
        else:
            error = model.lastError().text()

            QMessageBox.critical(self, "erreur 1", error)


    def nvl_oblig(self):

        #Fonction permet d'insérer les champs rentrés par l'utilisateur dans la base de donneés ACCESS
        date = self.calendarWidget.selectedDate()
        #Mise en forme de la date
        if len(str(date.day())) < 2:
            day2 = "0" + str(date.day())
        else: day2 = str(date.day())

        if len(str(date.month())) <2:
            month2 = "0" +str(date.month())
        else: month2 = str(date.month())
        datestr = str(day2) + "/" + str(month2) + "/" + str(date.year())

        model = self.modelObligation
        new_row = model.record()

        #Récupération des données saisies par l'utilisateur
        ISIN = "'" + self.lineEdit_ISIN.text() +"'"
        Nominal = self.lineEdit_Nominal.text()
        Cours = self.lineEdit_Cours.text()
        Coupon = self.lineEdit_Coupon.text()
        DevisePassee = self.lineEdit_DevisePassee.text()
        DevisePrst = self.lineEdit_DevisePrst.text()
        Libelle = "'" + self.lineEdit_Libelle.text() +"'"
        Rendement =self.lineEdit_Rendement.text()
        Duration =self.lineEdit_Duration.text()
        #TODO rajouter classe duration
        SpreadBund =self.lineEdit_SpreadBund.text()
        #TODO rajouter interets courus
        Sensibilite =self.lineEdit_Sensibilite.text()
        Convexite = self.lineEdit_Convexite.text()
        AvgLife =self.lineEdit_AvgLife.text()
        Indexation =self.lineEdit_Indexation.text()

        Ticker =  "'"+ self.comboBox_Ticker.currentText() +"'"
        Rating = "'" + self.comboBox_Rating.currentText() +"'"
        RatingSP = "'" + self.comboBox_RatingSP.currentText() + "'"
        RatingMoody = "'" + self.comboBox_RatingMoody.currentText() +"'"
        RatingFitch = "'"+ self.comboBox_RatingFitch.currentText() +"'"

        #Puis celle qui nécéssitent une autre table
        Type = self.comboBox_Type.currentText()
        if Type != '':
            qType =  QtSql.QSqlQuery()
            rType = qType.exec("SELECT noType FROM TypeOblig WHERE nomType = '" + Type +"'")
            if qType.first():
                sType = "'" + str(qType.value(0)) + "'"
        else: sType  = 0

        Region = self.comboBox_Region.currentText()
        if Region != '':
            qRegion =  QtSql.QSqlQuery()
            rRegion = qRegion.exec("SELECT noRegion FROM Region WHERE nomRegion = '" + Region +"'")
            if qRegion.first():
                sRegion = "'" + str(qRegion.value(0)) +"'"
        else : sRegion = 0

        Ssecteur = self.comboBox_SsSecteur.currentText()
        if Ssecteur != '':
            qSsecteur =  QtSql.QSqlQuery()
            rSsecteur = qSsecteur.exec("SELECT noSousSecteur FROM SousSecteur WHERE nomSousSecteur = '" + Ssecteur +"'")
            if qSsecteur.first():
                sSsecteur = "'" + str(qSsecteur.value(0)) +"'"
        else : sSsecteur =0

        Maturite  = self.comboBox_Maturite.currentText()
        ClasseDuration = self.comboBox_ClasseDuration.currentText() #???



        Tstr=[]
        T=[]

        L = [ISIN, Libelle, Ticker, Nominal, Cours, Coupon, DevisePassee, DevisePrst, Rendement, Duration, SpreadBund, Sensibilite, Convexite, AvgLife, Indexation, Rating, RatingSP, RatingMoody, RatingFitch, sRegion, sSsecteur, sType]
        Lstr = ['ISIN', 'Libelle', 'Ticker', 'Nominal', 'Cours', 'Coupon', 'DeviseAchat', 'DeviseConversion', 'Rendement', 'Duration', 'SpreadBund', 'Sensibilite', 'Convexite', 'VieMoyenne', 'Indexation', 'Rating', 'RatingSP', 'RatingMoody', 'RatingFitch', 'noRegion', 'noSousSecteur', 'noType']


        #On va construire la requête SQL avec une liste contenant les champs
        for index in range(len(L)):
            if L[index] != '':
                T.append(L[index])
                Tstr.append(Lstr[index])
        s='('
        s2='('
        for index in range(len(Tstr)-1):
            s  = s+ Tstr[index] + ', '
            s2 = s2 + str(T[index]) + ', '
        s = s + Tstr[-1] + ')'
        s2 = s2 + str(T[-1]) + ')'

        qinsert = QtSql.QSqlQuery()
        rinsert = qinsert.exec("INSERT INTO obligation " + s + " VALUES " + s2)


        if rinsert:
            QMessageBox.information(self, "Nouveau Client", "Ajout réussi")
        else:
            error = model.lastError().text()
            QMessageBox.critical(self, "Database returned an error", error)






