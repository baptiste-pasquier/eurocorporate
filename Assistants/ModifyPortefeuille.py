from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtSql
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QInputDialog, QMessageBox


from Assistants.ModifyPortefeuilleUI import Ui_DialogModifyPortefeuille


class WindowModifyPortefeuille(QtWidgets.QDialog, Ui_DialogModifyPortefeuille):
    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)
    