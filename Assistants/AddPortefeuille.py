from PyQt5 import QtWidgets

from Assistants.AddPortefeuilleUI import Ui_DialogAddPortefeuille


class WindowAddPortefeuille(QtWidgets.QDialog, Ui_DialogAddPortefeuille):
    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)
