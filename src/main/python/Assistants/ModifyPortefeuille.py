from PyQt5 import QtWidgets


from Assistants.ModifyPortefeuilleUI import Ui_DialogModifyPortefeuille


class WindowModifyPortefeuille(QtWidgets.QDialog, Ui_DialogModifyPortefeuille):
    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)
