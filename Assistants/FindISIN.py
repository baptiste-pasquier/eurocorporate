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
            obligation = Obligation()
            obligation.ISIN = str(query.value(0))
            obligation.Libelle = str(query.value(1))
            self.listeISIN.append(obligation)
        query.clear()

        for obligation in self.listeISIN:
            self.listWidget.addItem(obligation.ISIN + "  |  " + obligation.Libelle)

        self.tb_ISIN.textChanged.connect(self.tb_ISIN_changed)
        self.tb_libelle.textChanged.connect(self.tb_libelle_changed)
        self.listWidget.currentRowChanged.connect(self.row_changed)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.result = None

    def tb_ISIN_changed(self):
        if len(self.tb_ISIN.text()) > 0:
            if len(self.tb_libelle.text()) > 0:
                self.tb_libelle.setText("")
            compteur = 0
            for i in range(len(self.listeISIN)):
                compteur += 1
                if re.match("^" + self.tb_ISIN.text().lower() + ".*", self.listeISIN[i].ISIN.lower()):
                    self.listWidget.item(i).setHidden(False)
                else:
                    self.listWidget.item(i).setHidden(True)
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
                if re.match("^" + self.tb_libelle.text().lower() + ".*", self.listeISIN[i].Libelle.lower()):
                    self.listWidget.item(i).setHidden(False)
                else:
                    self.listWidget.item(i).setHidden(True)
        else:
            if len(self.tb_ISIN.text()) == 0:
                for i in range(len(self.listeISIN)):
                    self.listWidget.item(i).setHidden(False)

    def row_changed(self, row):
        if row > -1:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            self.result = self.listeISIN[row].ISIN
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            self.result = None
