from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir, QSettings, QCoreApplication
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Gestionnaires.GestionnaireEtatUI import Ui_MainWindowEtat


class MainWindowEtat(QtWidgets.QMainWindow, Ui_MainWindowEtat):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        Ui_MainWindowEtat.__init__(self)
        self.setupUi(self)
