import sys
from PyQt5 import QtCore, QtWidgets, uic

from portefeuille import MainWindowPortefeuille

qt_creator_file = "MainMenu.ui"
Ui_MainWindowMenu, QtBaseClass = uic.loadUiType(qt_creator_file)
# import MainMenuUI
# from MainMenuUI import Ui_MainWindowMenu

class MainWindowMenu(QtWidgets.QMainWindow, Ui_MainWindowMenu):
    
    switch_window = QtCore.pyqtSignal()
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindowMenu.__init__(self)
        self.setupUi(self)

        self.pushButton_Portefeuille.clicked.connect(self.switchPortefeuille)


    def switchPortefeuille(self):
        self.switch_window.emit()


class Controller:

    def __init__(self):
        pass

    def show_main_menu(self):
        self.main_menu = MainWindowMenu()
        self.main_menu.switch_window.connect(self.show_portefeuille)
        self.main_menu.show()


    def show_portefeuille(self):
        self.portefeuille = MainWindowPortefeuille()
        # self.portefeuille.switch_window.connect(self.show_window_two)
        self.main_menu.close()
        self.portefeuille.show()

    

app = QtWidgets.QApplication(sys.argv)
controller = Controller()
controller.show_main_menu()
sys.exit(app.exec_())

