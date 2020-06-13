import sys
from PyQt5 import QtWidgets, uic, QtCore
from Tools.database import createconnection
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QSettings, QDir

from Gestionnaires.GestionnairePortefeuille import MainWindowPortefeuille

qt_creator_file = "MainMenu.ui"
Ui_MainWindowMenu, QtBaseClass = uic.loadUiType(qt_creator_file)


class MainWindowMenu(QtWidgets.QMainWindow, Ui_MainWindowMenu):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindowMenu.__init__(self)
        self.setupUi(self)

        self.btn_config.clicked.connect(self.config)

    def config(self):
        QMessageBox.information(self, "Configuration", "Sélectionner la base de données")
        settings = QSettings()
        BDD = settings.value("BDD", defaultValue='')
        if BDD == '':
            file = QFileDialog.getOpenFileName(self)[0]
        else:
            file = QFileDialog.getOpenFileName(self, directory=QDir(BDD).path())[0]

        if file != '':
            settings = QSettings()
            settings.setValue("BDD", file)
            QMessageBox.warning(self, "Configuration", "Relancer l'application pour prendre en compte le changement")


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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    QtCore.QCoreApplication.setOrganizationName("ENSAE Junior Etudes")
    # QtCore.QCoreApplication.setOrganizationDomain("")
    QtCore.QCoreApplication.setApplicationName("IS")
    controller = Controller()
    controller.show_main_menu()
    sys.exit(app.exec_())
