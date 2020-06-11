import sys
from PyQt5 import QtWidgets, uic
from Tools.database import createconnection

from Gestionnaires.GestionnairePortefeuille import MainWindowPortefeuille

qt_creator_file = "MainMenu.ui"
Ui_MainWindowMenu, QtBaseClass = uic.loadUiType(qt_creator_file)
# import MainMenuUI
# from MainMenuUI import Ui_MainWindowMenu


class MainWindowMenu(QtWidgets.QMainWindow, Ui_MainWindowMenu):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindowMenu.__init__(self)
        self.setupUi(self)


class Controller:

    def __init__(self):
        createconnection()
        pass

    def show_main_menu(self):
        self.main_menu = MainWindowMenu()
        self.main_menu.pushButton_Portefeuille.clicked.connect(self.show_portefeuille)

        self.main_menu.show()

    def show_portefeuille(self):
        self.portefeuille_window = MainWindowPortefeuille()
        # self.main_menu.close()

        self.portefeuille_window.show()


app = QtWidgets.QApplication(sys.argv)
controller = Controller()
controller.show_main_menu()
sys.exit(app.exec_())
