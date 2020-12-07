# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AssistantClient.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindowClient(object):
    def setupUi(self, MainWindowClient):
        MainWindowClient.setObjectName("MainWindowClient")
        MainWindowClient.setWindowModality(QtCore.Qt.WindowModal)
        MainWindowClient.resize(547, 469)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ressources/img/icone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindowClient.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindowClient)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget_Valider = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_Valider.setObjectName("tabWidget_Valider")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_Entreprise = QtWidgets.QLabel(self.tab)
        self.label_Entreprise.setObjectName("label_Entreprise")
        self.verticalLayout_5.addWidget(self.label_Entreprise)
        self.label_Name = QtWidgets.QLabel(self.tab)
        self.label_Name.setObjectName("label_Name")
        self.verticalLayout_5.addWidget(self.label_Name)
        self.label_Forename = QtWidgets.QLabel(self.tab)
        self.label_Forename.setObjectName("label_Forename")
        self.verticalLayout_5.addWidget(self.label_Forename)
        self.label_Mail = QtWidgets.QLabel(self.tab)
        self.label_Mail.setObjectName("label_Mail")
        self.verticalLayout_5.addWidget(self.label_Mail)
        self.label_Tel = QtWidgets.QLabel(self.tab)
        self.label_Tel.setObjectName("label_Tel")
        self.verticalLayout_5.addWidget(self.label_Tel)
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_5.addItem(spacerItem)
        self.label_Comment = QtWidgets.QLabel(self.tab)
        self.label_Comment.setObjectName("label_Comment")
        self.verticalLayout_5.addWidget(self.label_Comment)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_5.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lineEdit_Entreprise = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_Entreprise.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_Entreprise.setObjectName("lineEdit_Entreprise")
        self.verticalLayout_6.addWidget(self.lineEdit_Entreprise)
        self.lineEdit_ContactName = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_ContactName.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_ContactName.setObjectName("lineEdit_ContactName")
        self.verticalLayout_6.addWidget(self.lineEdit_ContactName)
        self.lineEdit_ContactForename = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_ContactForename.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_ContactForename.setObjectName("lineEdit_ContactForename")
        self.verticalLayout_6.addWidget(self.lineEdit_ContactForename)
        self.lineEdit_Mail = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_Mail.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_Mail.setObjectName("lineEdit_Mail")
        self.verticalLayout_6.addWidget(self.lineEdit_Mail)
        self.lineEdit_Tel = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_Tel.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_Tel.setObjectName("lineEdit_Tel")
        self.verticalLayout_6.addWidget(self.lineEdit_Tel)
        self.textEdit_Comment = QtWidgets.QTextEdit(self.tab)
        self.textEdit_Comment.setObjectName("textEdit_Comment")
        self.verticalLayout_6.addWidget(self.textEdit_Comment)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 114, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.pushButton_Valider = QtWidgets.QPushButton(self.tab)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ressources/img/checked-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Valider.setIcon(icon1)
        self.pushButton_Valider.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_Valider.setObjectName("pushButton_Valider")
        self.horizontalLayout_4.addWidget(self.pushButton_Valider)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        spacerItem5 = QtWidgets.QSpacerItem(20, 113, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem5)
        self.tabWidget_Valider.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox_ModClient = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_ModClient.setMinimumSize(QtCore.QSize(0, 26))
        self.comboBox_ModClient.setObjectName("comboBox_ModClient")
        self.verticalLayout.addWidget(self.comboBox_ModClient)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labe_ModEntreprise = QtWidgets.QLabel(self.tab_2)
        self.labe_ModEntreprise.setObjectName("labe_ModEntreprise")
        self.verticalLayout_2.addWidget(self.labe_ModEntreprise)
        self.label_ModContactName = QtWidgets.QLabel(self.tab_2)
        self.label_ModContactName.setObjectName("label_ModContactName")
        self.verticalLayout_2.addWidget(self.label_ModContactName)
        self.label_ModContactForename = QtWidgets.QLabel(self.tab_2)
        self.label_ModContactForename.setObjectName("label_ModContactForename")
        self.verticalLayout_2.addWidget(self.label_ModContactForename)
        self.label_ModMail = QtWidgets.QLabel(self.tab_2)
        self.label_ModMail.setObjectName("label_ModMail")
        self.verticalLayout_2.addWidget(self.label_ModMail)
        self.label_ModTel = QtWidgets.QLabel(self.tab_2)
        self.label_ModTel.setObjectName("label_ModTel")
        self.verticalLayout_2.addWidget(self.label_ModTel)
        spacerItem6 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem6)
        self.label_ModComment = QtWidgets.QLabel(self.tab_2)
        self.label_ModComment.setObjectName("label_ModComment")
        self.verticalLayout_2.addWidget(self.label_ModComment)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem7)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lineEdit_ModEntreprise = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_ModEntreprise.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_ModEntreprise.setObjectName("lineEdit_ModEntreprise")
        self.verticalLayout_4.addWidget(self.lineEdit_ModEntreprise)
        self.lineEdit_ModContactName = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_ModContactName.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_ModContactName.setObjectName("lineEdit_ModContactName")
        self.verticalLayout_4.addWidget(self.lineEdit_ModContactName)
        self.lineEdit_ModContactForename = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_ModContactForename.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_ModContactForename.setObjectName("lineEdit_ModContactForename")
        self.verticalLayout_4.addWidget(self.lineEdit_ModContactForename)
        self.lineEdit_ModMail = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_ModMail.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_ModMail.setObjectName("lineEdit_ModMail")
        self.verticalLayout_4.addWidget(self.lineEdit_ModMail)
        self.lineEdit_ModTel = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_ModTel.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_ModTel.setObjectName("lineEdit_ModTel")
        self.verticalLayout_4.addWidget(self.lineEdit_ModTel)
        self.textEdit_ModComment = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit_ModComment.setObjectName("textEdit_ModComment")
        self.verticalLayout_4.addWidget(self.textEdit_ModComment)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_8.addLayout(self.verticalLayout)
        spacerItem8 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem8)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem9)
        self.pushButton_ModValider = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_ModValider.setIcon(icon1)
        self.pushButton_ModValider.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_ModValider.setObjectName("pushButton_ModValider")
        self.horizontalLayout_5.addWidget(self.pushButton_ModValider)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem10)
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)
        spacerItem11 = QtWidgets.QSpacerItem(20, 99, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem11)
        self.tabWidget_Valider.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.comboBox_SupprClient = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_SupprClient.setMinimumSize(QtCore.QSize(0, 26))
        self.comboBox_SupprClient.setObjectName("comboBox_SupprClient")
        self.verticalLayout_9.addWidget(self.comboBox_SupprClient)
        spacerItem12 = QtWidgets.QSpacerItem(20, 139, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem12)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem13)
        self.pushButton_SupprValider = QtWidgets.QPushButton(self.tab_3)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/ressources/img/delete-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_SupprValider.setIcon(icon2)
        self.pushButton_SupprValider.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_SupprValider.setObjectName("pushButton_SupprValider")
        self.horizontalLayout_3.addWidget(self.pushButton_SupprValider)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem14)
        self.verticalLayout_9.addLayout(self.horizontalLayout_3)
        spacerItem15 = QtWidgets.QSpacerItem(20, 138, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem15)
        self.tabWidget_Valider.addTab(self.tab_3, "")
        self.verticalLayout_3.addWidget(self.tabWidget_Valider)
        MainWindowClient.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindowClient)
        self.statusbar.setObjectName("statusbar")
        MainWindowClient.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindowClient)
        self.tabWidget_Valider.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindowClient)

    def retranslateUi(self, MainWindowClient):
        _translate = QtCore.QCoreApplication.translate
        MainWindowClient.setWindowTitle(_translate("MainWindowClient", "Assistant Client"))
        self.label_Entreprise.setText(_translate("MainWindowClient", "Entreprise"))
        self.label_Name.setText(_translate("MainWindowClient", "Nom du contact"))
        self.label_Forename.setText(_translate("MainWindowClient", "Prénom du Contact"))
        self.label_Mail.setText(_translate("MainWindowClient", "Mail du Contact"))
        self.label_Tel.setText(_translate("MainWindowClient", "N° de Tél."))
        self.label_Comment.setText(_translate("MainWindowClient", "Commentaires"))
        self.pushButton_Valider.setText(_translate("MainWindowClient", "Valider"))
        self.tabWidget_Valider.setTabText(self.tabWidget_Valider.indexOf(self.tab), _translate("MainWindowClient", "Client"))
        self.labe_ModEntreprise.setText(_translate("MainWindowClient", "Entreprise"))
        self.label_ModContactName.setText(_translate("MainWindowClient", "Nom du Contact"))
        self.label_ModContactForename.setText(_translate("MainWindowClient", "Prénom du Contact"))
        self.label_ModMail.setText(_translate("MainWindowClient", "E-Mail"))
        self.label_ModTel.setText(_translate("MainWindowClient", "N° de Tél."))
        self.label_ModComment.setText(_translate("MainWindowClient", "Commentaires"))
        self.pushButton_ModValider.setText(_translate("MainWindowClient", "Valider"))
        self.tabWidget_Valider.setTabText(self.tabWidget_Valider.indexOf(self.tab_2), _translate("MainWindowClient", "Modifier un Client"))
        self.pushButton_SupprValider.setText(_translate("MainWindowClient", "Supprimer"))
        self.tabWidget_Valider.setTabText(self.tabWidget_Valider.indexOf(self.tab_3), _translate("MainWindowClient", "Supprimer un Client"))
import ressources_rc