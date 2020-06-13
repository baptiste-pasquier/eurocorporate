from PyQt5 import QtWidgets, QtSql
from PyQt5.QtWidgets import QDialogButtonBox
import re


from Assistants.FindISINUI import Ui_DialogFindISIN
from Classes.obligation import Obligation


class WindowFindISIN(QtWidgets.QDialog, Ui_DialogFindISIN):
    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.listeISIN = []

        query = QtSql.QSqlQuery()
        query.exec("SELECT DISTINCT ISIN, Libelle FROM Obligation ORDER BY ISIN ASC")
        while query.next():
            oblig = Obligation()
            oblig.ISIN = str(query.value(0))
            oblig.Libelle = str(query.value(1))
            self.listeISIN.append(oblig)
        query.clear()

        for oblig in self.listeISIN:
            self.listWidget.addItem(oblig.ISIN + "  |  " + oblig.Libelle)

        self.tb_ISIN.textChanged.connect(self.tb_ISIN_changed)
        self.tb_libelle.textChanged.connect(self.tb_libelle_changed)
        self.listWidget.currentRowChanged.connect(self.row_changed)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.resul = None

    def tb_ISIN_changed(self):
        if len(self.tb_ISIN.text()) > 0:
            if len(self.tb_libelle.text()) > 0:
                self.tb_libelle.setText("")
            compteur = 0
            for i in range(len(self.listeISIN)):
                compteur += 1
                if re.match("^" + self.tb_ISIN.text() + ".*", self.listeISIN[i].ISIN):
                    self.listWidget.item(i).setHidden(False)
                else:
                    self.listWidget.item(i).setHidden(True)
            print("ISIN " + str(compteur))
        else:
            if len(self.tb_libelle.text()) == 0:
                for i in range(len(self.listeISIN)):
                    self.listWidget.item(i).setHidden(False)

    def tb_libelle_changed(self):
        if len(self.tb_libelle.text()) > 0:
            if len(self.tb_ISIN.text()) > 0:
                self.tb_ISIN.setText("")
            compteur = 0
            for i in range(len(self.listeISIN)):
                compteur += 1
                if re.match("^" + self.tb_libelle.text() + ".*", self.listeISIN[i].Libelle):
                    self.listWidget.item(i).setHidden(False)
                else:
                    self.listWidget.item(i).setHidden(True)
            print("Libelle " + str(compteur))
        else:
            if len(self.tb_ISIN.text()) == 0:
                for i in range(len(self.listeISIN)):
                    self.listWidget.item(i).setHidden(False)

    def row_changed(self, row):
        if row > -1:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            self.resul = self.listeISIN[row].ISIN
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            self.resul = None
