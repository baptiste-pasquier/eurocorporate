import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir, QSettings, QCoreApplication
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Gestionnaires.GestionnairePortefeuille import MainWindowPortefeuille
from Tools.database import createconnection

from MainMenuUI import Ui_MainWindowMenu

# fbs
# from fbs_runtime.application_context.PyQt5 import ApplicationContext


class MainWindowMenu(QtWidgets.QMainWindow, Ui_MainWindowMenu):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindowMenu.__init__(self)
        self.setupUi(self)

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
