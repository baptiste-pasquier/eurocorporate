from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtSql
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QInputDialog, QMessageBox


from Assistants.AddPortefeuilleUI import Ui_DialogAddPortefeuille


class WindowAddPortefeuille(QtWidgets.QDialog, Ui_DialogAddPortefeuille):
    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)
    