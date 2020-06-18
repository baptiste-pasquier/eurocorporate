import win32com.client as win32
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir, QSettings, QCoreApplication, pyqtSlot
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
        self.tb_date.setText(self.date.toString("dd/MM/yyyy"))

        self.strNoPort = str(portefeuilleChoisi.noPortefeuille)
        self.strDate = dateChoisie.toString("MM/dd/yyyy")
        self.legendePort = "Legende " + portefeuilleChoisi.nomPortefeuille

        settings = QSettings()
        self.fileBDD = settings.value("BDD")

    def imprimerEtat(self, nomEtat, whereCondition, legendePortefeuille):
        # Ouverture de la base de données
        acc = win32.gencache.EnsureDispatch('Access.Application')
        acc.OpenCurrentDatabase(self.fileBDD, True)
        acc.Visible = True
        # On ouvre l'"tat en mode preview le temps que l'utilisateur choisisse l'imprimante
        # acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewPreview, None, whereCondition)
        # acc.Reports.Item(nomEtat).Controls.Item("txt_nomportefeuille").Caption = legendePortefeuille
        acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewNormal, None, whereCondition)
        # On ferme la base de données
        # acc.CloseCurrentDatabase()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.imprimerEtat("ExigenceCapital", "[noPortefeuille] = " + self.strNoPort + "  AND DateDeMAJ = #" + self.strDate + "#", self.legendePort)
