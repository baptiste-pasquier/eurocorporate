# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainMenu.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindowMenu(object):
    def setupUi(self, MainWindowMenu):
        MainWindowMenu.setObjectName("MainWindowMenu")
        MainWindowMenu.resize(700, 600)
        MainWindowMenu.setMinimumSize(QtCore.QSize(700, 600))
        MainWindowMenu.setMaximumSize(QtCore.QSize(700, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ressources/img/icone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindowMenu.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindowMenu)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/ressources/img/icone long.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_Oblig = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_Oblig.setMinimumSize(QtCore.QSize(0, 50))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ressources/img/paper-money-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Oblig.setIcon(icon1)
        self.pushButton_Oblig.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_Oblig.setObjectName("pushButton_Oblig")
        self.verticalLayout_2.addWidget(self.pushButton_Oblig)
        spacerItem = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem)
        self.pushButton_Client = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_Client.setMinimumSize(QtCore.QSize(0, 50))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/ressources/img/client-management-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Client.setIcon(icon2)
        self.pushButton_Client.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_Client.setObjectName("pushButton_Client")
        self.verticalLayout_2.addWidget(self.pushButton_Client)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem1)
        self.pushButton_Portefeuille = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_Portefeuille.setMinimumSize(QtCore.QSize(0, 50))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/ressources/img/wallet-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Portefeuille.setIcon(icon3)
        self.pushButton_Portefeuille.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_Portefeuille.setObjectName("pushButton_Portefeuille")
        self.verticalLayout_2.addWidget(self.pushButton_Portefeuille)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 127))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_IS_BEC = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_IS_BEC.setMinimumSize(QtCore.QSize(0, 50))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/ressources/img/microsoft-access-2019-240.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_IS_BEC.setIcon(icon4)
        self.pushButton_IS_BEC.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_IS_BEC.setObjectName("pushButton_IS_BEC")
        self.gridLayout_2.addWidget(self.pushButton_IS_BEC, 0, 1, 1, 1)
        self.pushButton_CreationAccess = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_CreationAccess.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_CreationAccess.setIcon(icon4)
        self.pushButton_CreationAccess.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_CreationAccess.setObjectName("pushButton_CreationAccess")
        self.gridLayout_2.addWidget(self.pushButton_CreationAccess, 0, 0, 1, 1)
        self.btn_config = QtWidgets.QPushButton(self.groupBox)
        self.btn_config.setMinimumSize(QtCore.QSize(0, 30))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/ressources/img/settings-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_config.setIcon(icon5)
        self.btn_config.setObjectName("btn_config")
        self.gridLayout_2.addWidget(self.btn_config, 1, 0, 1, 1)
        self.btn_config_2 = QtWidgets.QPushButton(self.groupBox)
        self.btn_config_2.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_config_2.setIcon(icon5)
        self.btn_config_2.setObjectName("btn_config_2")
        self.gridLayout_2.addWidget(self.btn_config_2, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        MainWindowMenu.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindowMenu)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        MainWindowMenu.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindowMenu)
        QtCore.QMetaObject.connectSlotsByName(MainWindowMenu)

    def retranslateUi(self, MainWindowMenu):
        _translate = QtCore.QCoreApplication.translate
        MainWindowMenu.setWindowTitle(_translate("MainWindowMenu", "Menu principal"))
        self.groupBox_2.setTitle(_translate("MainWindowMenu", "Assistants"))
        self.pushButton_Oblig.setText(_translate("MainWindowMenu", "Assistant de gestion Obligataire"))
        self.pushButton_Client.setText(_translate("MainWindowMenu", "Assistant de gestion : Client"))
        self.pushButton_Portefeuille.setText(_translate("MainWindowMenu", "Assistant de gestion : Portefeuille"))
        self.groupBox.setTitle(_translate("MainWindowMenu", "Access"))
        self.pushButton_IS_BEC.setText(_translate("MainWindowMenu", "Accéder à Access (IS_beC)"))
        self.pushButton_CreationAccess.setText(_translate("MainWindowMenu", "Accéder à Access (ISC_beC)"))
        self.btn_config.setText(_translate("MainWindowMenu", "Configuration (ISC_beC)"))
        self.btn_config_2.setText(_translate("MainWindowMenu", "Configuration (IS_beC)"))
import ressources_rc
