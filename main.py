import sys
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir, QSettings, QCoreApplication, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Assistants.AssistantClient import MainWindowClient
from Gestionnaires.GestionnairePortefeuille import MainWindowPortefeuille
# from Gestionnaires.GestionnaireObligataire import MainWindowObligation
from Tools.database import createconnection

from MainMenuUI import Ui_MainWindowMenu

# fbs
# from fbs_runtime.application_context.PyQt5 import ApplicationContext


class MainWindowMenu(QtWidgets.QMainWindow, Ui_MainWindowMenu):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindowMenu.__init__(self)
        self.setupUi(self)

        settings = QSettings()
        BDD = settings.value("BDD", defaultValue='')
        BDD_IS_BEC = settings.value("BDD_IS_BEC", defaultValue='')
        self.btn_config.setStatusTip(BDD)
        self.btn_config_2.setStatusTip(BDD_IS_BEC)
        self.pushButton_CreationAccess.setStatusTip(BDD)
        self.pushButton_IS_BEC.setStatusTip(BDD_IS_BEC)

        self.btn_config.clicked.connect(self.config)
        self.btn_config_2.clicked.connect(self.config2)

    def config(self):
        QMessageBox.information(self, "Configuration", "Sélectionner la base de données ISC_BeC (contenant la requête et les états)")
        settings = QSettings()
        BDD = settings.value("BDD", defaultValue='')
        if BDD == '':
            fileName = QFileDialog.getOpenFileName(self)[0]
        else:
            fileName = QFileDialog.getOpenFileName(self, directory=QDir(BDD).path())[0]

        if fileName:
            settings = QSettings()
            settings.setValue("BDD", fileName)
            QMessageBox.warning(self, "Configuration", "Relancer l'application pour prendre en compte le changement")

    def config2(self):
        QMessageBox.information(self, "Configuration", "Sélectionner la base de données IS_BeC")
        settings = QSettings()
        BDD_IS_BEC = settings.value("BDD_IS_BEC", defaultValue='')
        if BDD_IS_BEC == '':
            fileName = QFileDialog.getOpenFileName(self)[0]
        else:
            fileName = QFileDialog.getOpenFileName(self, directory=QDir(BDD_IS_BEC).path())[0]

        if fileName:
            settings = QSettings()
            settings.setValue("BDD_IS_BEC", fileName)
            QMessageBox.warning(self, "Configuration", "Changement réussi")

    @pyqtSlot()
    def on_pushButton_IS_BEC_clicked(self):
        settings = QSettings()
        BDD_IS_BEC = settings.value("BDD_IS_BEC", defaultValue='')
        if BDD_IS_BEC:
            os.startfile(BDD_IS_BEC)
        else:
            QMessageBox.critical(self, "Base Access inconnue", "Veuillez configurer la base Access et relancer l'application")

    @pyqtSlot()
    def on_pushButton_CreationAccess_clicked(self):
        settings = QSettings()
        BDD = settings.value("BDD", defaultValue='')
        if BDD:
            os.startfile(BDD)
        else:
            QMessageBox.critical(self, "Base Access inconnue", "Veuillez configurer la base Access et relancer l'application")


class Controller:

    def __init__(self):
        createconnection()
        pass

    def show_main_menu(self):
        self.main_menu = MainWindowMenu()

        self.main_menu.pushButton_Oblig.clicked.connect(self.show_obligation)
        self.main_menu.pushButton_Client.clicked.connect(self.show_client)
        self.main_menu.pushButton_Portefeuille.clicked.connect(self.show_portefeuille)

        self.main_menu.show()

    def show_obligation(self):
        self.obligation_window = MainWindowObligation(self.main_menu)
        self.obligation_window.show()

    def show_client(self):
        self.client_window = MainWindowClient(self.main_menu)
        self.client_window.show()

    def show_portefeuille(self):
        self.portefeuille_window = MainWindowPortefeuille(self.main_menu)
        # self.main_menu.close()
        self.portefeuille_window.show()


if __name__ == '__main__':
    # fbs
    # appctxt = ApplicationContext()
    # python
    app = QtWidgets.QApplication(sys.argv)

    QtCore.QCoreApplication.setOrganizationName("ENSAE Junior Etudes")
    QtCore.QCoreApplication.setApplicationName("Eurocorporate IS")

    locale = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    reptrad = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    translator.load("qtbase_" + locale, reptrad)  # qtbase_fr.qm
    QCoreApplication.installTranslator(translator)

    controller = Controller()
    controller.show_main_menu()

    # python
    sys.exit(app.exec_())
    # fbs
    # exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    # sys.exit(exit_code)
