# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FicheClient.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindowFicheClient(object):
    def setupUi(self, MainWindowFicheClient):
        MainWindowFicheClient.setObjectName("MainWindowFicheClient")
        MainWindowFicheClient.setWindowModality(QtCore.Qt.WindowModal)
        MainWindowFicheClient.resize(584, 497)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ressources/img/icone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindowFicheClient.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindowFicheClient)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(110, 0))
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox_Client = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_Client.setMinimumSize(QtCore.QSize(0, 26))
        self.comboBox_Client.setObjectName("comboBox_Client")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_Client)
        self.verticalLayout.addLayout(self.formLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_Entreprise_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_Entreprise_2.setObjectName("label_Entreprise_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_Entreprise_2)
        self.lineEdit_Entreprise = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Entreprise.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_Entreprise.setObjectName("lineEdit_Entreprise")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Entreprise)
        self.label_Name_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_Name_2.setObjectName("label_Name_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_Name_2)
        self.lineEdit_ContactName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_ContactName.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_ContactName.setObjectName("lineEdit_ContactName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_ContactName)
        self.label_Forename_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_Forename_2.setMinimumSize(QtCore.QSize(110, 0))
        self.label_Forename_2.setObjectName("label_Forename_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_Forename_2)
        self.lineEdit_ContactForename = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_ContactForename.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_ContactForename.setObjectName("lineEdit_ContactForename")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_ContactForename)
        self.label_Mail_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_Mail_2.setObjectName("label_Mail_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_Mail_2)
        self.lineEdit_Mail = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Mail.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_Mail.setObjectName("lineEdit_Mail")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Mail)
        self.label_Mail_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_Mail_3.setObjectName("label_Mail_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_Mail_3)
        self.lineEdit_Mail_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Mail_2.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_Mail_2.setObjectName("lineEdit_Mail_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Mail_2)
        self.label_Mail_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_Mail_4.setObjectName("label_Mail_4")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_Mail_4)
        self.textEdit_Commentaires = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEdit_Commentaires.setReadOnly(True)
        self.textEdit_Commentaires.setObjectName("textEdit_Commentaires")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.textEdit_Commentaires)
        self.verticalLayout.addLayout(self.formLayout)
        MainWindowFicheClient.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindowFicheClient)
        self.statusbar.setObjectName("statusbar")
        MainWindowFicheClient.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindowFicheClient)
        QtCore.QMetaObject.connectSlotsByName(MainWindowFicheClient)

    def retranslateUi(self, MainWindowFicheClient):
        _translate = QtCore.QCoreApplication.translate
        MainWindowFicheClient.setWindowTitle(_translate("MainWindowFicheClient", "Fiche Client"))
        self.label.setText(_translate("MainWindowFicheClient", "Client"))
        self.label_Entreprise_2.setText(_translate("MainWindowFicheClient", "Entreprise"))
        self.label_Name_2.setText(_translate("MainWindowFicheClient", "Nom du contact"))
        self.label_Forename_2.setText(_translate("MainWindowFicheClient", "Prénom du Contact"))
        self.label_Mail_2.setText(_translate("MainWindowFicheClient", "Mail du Contact"))
        self.label_Mail_3.setText(_translate("MainWindowFicheClient", "Mail du Contact"))
        self.label_Mail_4.setText(_translate("MainWindowFicheClient", "Commentaires"))
import ressources_rc
