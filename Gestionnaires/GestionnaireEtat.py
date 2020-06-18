from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir, QSettings, QCoreApplication
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from Classes.client import Client
from Classes.portefeuille import Portefeuille

from Gestionnaires.GestionnaireEtatUI import Ui_MainWindowEtat


class MainWindowEtat(QtWidgets.QMainWindow, Ui_MainWindowEtat):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        Ui_MainWindowEtat.__init__(self)
        self.setupUi(self)

    def init(self, clientChoisi, portefeuilleChoisi, dateChoisie):
        self.client = clientChoisi
        self.portefeuille = portefeuilleChoisi
        self.date = dateChoisie

        self.tb_client.setText(str(self.client.noClient) + " - " + self.client.nomEntreprise)
        self.tb_portefeuille.setText(str(self.portefeuille.noPortefeuille) + " - " + self.portefeuille.nomPortefeuille)
        self.tb_date.setText(self.date.toString("dd/MM/yy"))

    