# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GestionnairePortefeuille.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindowPortefeuille(object):
    def setupUi(self, MainWindowPortefeuille):
        MainWindowPortefeuille.setObjectName("MainWindowPortefeuille")
        MainWindowPortefeuille.setWindowModality(QtCore.Qt.WindowModal)
        MainWindowPortefeuille.resize(1143, 849)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/icone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindowPortefeuille.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindowPortefeuille)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.btn_unlockClient = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_unlockClient.sizePolicy().hasHeightForWidth())
        self.btn_unlockClient.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ressources/img/unlock-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_unlockClient.setIcon(icon1)
        self.btn_unlockClient.setIconSize(QtCore.QSize(30, 20))
        self.btn_unlockClient.setObjectName("btn_unlockClient")
        self.gridLayout.addWidget(self.btn_unlockClient, 0, 3, 1, 1)
        self.comboBox_clients = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_clients.sizePolicy().hasHeightForWidth())
        self.comboBox_clients.setSizePolicy(sizePolicy)
        self.comboBox_clients.setMinimumSize(QtCore.QSize(0, 26))
        self.comboBox_clients.setObjectName("comboBox_clients")
        self.gridLayout.addWidget(self.comboBox_clients, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox_portefeuilles = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_portefeuilles.setMinimumSize(QtCore.QSize(300, 26))
        self.comboBox_portefeuilles.setObjectName("comboBox_portefeuilles")
        self.gridLayout.addWidget(self.comboBox_portefeuilles, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.btn_unlockPortefeuille = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_unlockPortefeuille.sizePolicy().hasHeightForWidth())
        self.btn_unlockPortefeuille.setSizePolicy(sizePolicy)
        self.btn_unlockPortefeuille.setIcon(icon1)
        self.btn_unlockPortefeuille.setIconSize(QtCore.QSize(30, 20))
        self.btn_unlockPortefeuille.setObjectName("btn_unlockPortefeuille")
        self.gridLayout.addWidget(self.btn_unlockPortefeuille, 1, 3, 1, 1)
        self.btn_chooseClient = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_chooseClient.sizePolicy().hasHeightForWidth())
        self.btn_chooseClient.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/ressources/img/checked-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_chooseClient.setIcon(icon2)
        self.btn_chooseClient.setIconSize(QtCore.QSize(30, 20))
        self.btn_chooseClient.setObjectName("btn_chooseClient")
        self.gridLayout.addWidget(self.btn_chooseClient, 0, 2, 1, 1)
        self.btn_choosePortefeuille = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_choosePortefeuille.sizePolicy().hasHeightForWidth())
        self.btn_choosePortefeuille.setSizePolicy(sizePolicy)
        self.btn_choosePortefeuille.setIcon(icon2)
        self.btn_choosePortefeuille.setIconSize(QtCore.QSize(30, 20))
        self.btn_choosePortefeuille.setObjectName("btn_choosePortefeuille")
        self.gridLayout.addWidget(self.btn_choosePortefeuille, 1, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_newPortefeuille = QtWidgets.QPushButton(self.groupBox)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/ressources/img/add-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_newPortefeuille.setIcon(icon3)
        self.btn_newPortefeuille.setIconSize(QtCore.QSize(30, 20))
        self.btn_newPortefeuille.setObjectName("btn_newPortefeuille")
        self.horizontalLayout.addWidget(self.btn_newPortefeuille)
        self.label_portefeuilleChoisi = QtWidgets.QLabel(self.groupBox)
        self.label_portefeuilleChoisi.setObjectName("label_portefeuilleChoisi")
        self.horizontalLayout.addWidget(self.label_portefeuilleChoisi)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.tb_liquidite = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_liquidite.sizePolicy().hasHeightForWidth())
        self.tb_liquidite.setSizePolicy(sizePolicy)
        self.tb_liquidite.setMinimumSize(QtCore.QSize(0, 26))
        self.tb_liquidite.setReadOnly(False)
        self.tb_liquidite.setObjectName("tb_liquidite")
        self.gridLayout_2.addWidget(self.tb_liquidite, 0, 1, 1, 1)
        self.btn_liquidite = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_liquidite.sizePolicy().hasHeightForWidth())
        self.btn_liquidite.setSizePolicy(sizePolicy)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/ressources/img/checkmark-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_liquidite.setIcon(icon4)
        self.btn_liquidite.setIconSize(QtCore.QSize(30, 20))
        self.btn_liquidite.setObjectName("btn_liquidite")
        self.gridLayout_2.addWidget(self.btn_liquidite, 0, 2, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btn_today = QtWidgets.QPushButton(self.groupBox)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/ressources/img/calendar-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_today.setIcon(icon5)
        self.btn_today.setIconSize(QtCore.QSize(30, 20))
        self.btn_today.setObjectName("btn_today")
        self.gridLayout_3.addWidget(self.btn_today, 0, 2, 1, 1)
        self.label_dateChoisie = QtWidgets.QLabel(self.groupBox)
        self.label_dateChoisie.setObjectName("label_dateChoisie")
        self.gridLayout_3.addWidget(self.label_dateChoisie, 0, 0, 1, 1)
        self.tb_dateChoisie = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_dateChoisie.sizePolicy().hasHeightForWidth())
        self.tb_dateChoisie.setSizePolicy(sizePolicy)
        self.tb_dateChoisie.setMinimumSize(QtCore.QSize(0, 26))
        self.tb_dateChoisie.setReadOnly(True)
        self.tb_dateChoisie.setObjectName("tb_dateChoisie")
        self.gridLayout_3.addWidget(self.tb_dateChoisie, 0, 1, 1, 1)
        self.btn_transfert = QtWidgets.QPushButton(self.groupBox)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/ressources/img/date-to-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_transfert.setIcon(icon6)
        self.btn_transfert.setIconSize(QtCore.QSize(30, 20))
        self.btn_transfert.setObjectName("btn_transfert")
        self.gridLayout_3.addWidget(self.btn_transfert, 0, 3, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.calendarWidget = CalendarWidgetPerso(self.groupBox)
        self.calendarWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarWidget.sizePolicy().hasHeightForWidth())
        self.calendarWidget.setSizePolicy(sizePolicy)
        self.calendarWidget.setObjectName("calendarWidget")
        self.horizontalLayout_3.addWidget(self.calendarWidget)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSortingEnabled(False)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.btn_import = QtWidgets.QPushButton(self.centralwidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/ressources/img/microsoft-excel-2019-240.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_import.setIcon(icon7)
        self.btn_import.setIconSize(QtCore.QSize(30, 30))
        self.btn_import.setObjectName("btn_import")
        self.horizontalLayout_7.addWidget(self.btn_import)
        self.btn_export = QtWidgets.QPushButton(self.centralwidget)
        self.btn_export.setIcon(icon7)
        self.btn_export.setIconSize(QtCore.QSize(30, 30))
        self.btn_export.setObjectName("btn_export")
        self.horizontalLayout_7.addWidget(self.btn_export)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.label_nbLignes = QtWidgets.QLabel(self.centralwidget)
        self.label_nbLignes.setMinimumSize(QtCore.QSize(200, 0))
        self.label_nbLignes.setObjectName("label_nbLignes")
        self.horizontalLayout_7.addWidget(self.label_nbLignes)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_libelle = QtWidgets.QLabel(self.groupBox_2)
        self.label_libelle.setText("")
        self.label_libelle.setObjectName("label_libelle")
        self.verticalLayout_4.addWidget(self.label_libelle)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.comboBox_ISIN = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_ISIN.setCurrentText("")
        self.comboBox_ISIN.setObjectName("comboBox_ISIN")
        self.horizontalLayout_6.addWidget(self.comboBox_ISIN)
        self.btn_search = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_search.sizePolicy().hasHeightForWidth())
        self.btn_search.setSizePolicy(sizePolicy)
        self.btn_search.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/ressources/img/search-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_search.setIcon(icon8)
        self.btn_search.setObjectName("btn_search")
        self.horizontalLayout_6.addWidget(self.btn_search)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.tb_nombre = QtWidgets.QLineEdit(self.groupBox_2)
        self.tb_nombre.setObjectName("tb_nombre")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.tb_nombre)
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.tb_prix = QtWidgets.QLineEdit(self.groupBox_2)
        self.tb_prix.setObjectName("tb_prix")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.tb_prix)
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.tb_valo = QtWidgets.QLineEdit(self.groupBox_2)
        self.tb_valo.setObjectName("tb_valo")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.tb_valo)
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setObjectName("label_12")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.tb_valoAcqui = QtWidgets.QLineEdit(self.groupBox_2)
        self.tb_valoAcqui.setObjectName("tb_valoAcqui")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.tb_valoAcqui)
        self.label_dateMAJ = QtWidgets.QLabel(self.groupBox_2)
        self.label_dateMAJ.setMinimumSize(QtCore.QSize(0, 22))
        self.label_dateMAJ.setText("")
        self.label_dateMAJ.setObjectName("label_dateMAJ")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_dateMAJ)
        self.label_nominal = QtWidgets.QLabel(self.groupBox_2)
        self.label_nominal.setMinimumSize(QtCore.QSize(0, 22))
        self.label_nominal.setText("")
        self.label_nominal.setObjectName("label_nominal")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.label_nominal)
        self.verticalLayout_4.addLayout(self.formLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem4)
        self.btn_add = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_add.setIcon(icon3)
        self.btn_add.setIconSize(QtCore.QSize(30, 20))
        self.btn_add.setObjectName("btn_add")
        self.verticalLayout_4.addWidget(self.btn_add)
        self.btn_modif = QtWidgets.QPushButton(self.groupBox_2)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/ressources/img/edit-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_modif.setIcon(icon9)
        self.btn_modif.setIconSize(QtCore.QSize(30, 20))
        self.btn_modif.setObjectName("btn_modif")
        self.verticalLayout_4.addWidget(self.btn_modif)
        self.btn_suppr = QtWidgets.QPushButton(self.groupBox_2)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/ressources/img/delete-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_suppr.setIcon(icon10)
        self.btn_suppr.setIconSize(QtCore.QSize(30, 20))
        self.btn_suppr.setObjectName("btn_suppr")
        self.verticalLayout_4.addWidget(self.btn_suppr)
        self.btn_vis = QtWidgets.QPushButton(self.groupBox_2)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/ressources/img/statistics-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_vis.setIcon(icon11)
        self.btn_vis.setIconSize(QtCore.QSize(30, 30))
        self.btn_vis.setObjectName("btn_vis")
        self.verticalLayout_4.addWidget(self.btn_vis)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        MainWindowPortefeuille.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowPortefeuille)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1143, 26))
        self.menubar.setObjectName("menubar")
        MainWindowPortefeuille.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowPortefeuille)
        self.statusbar.setObjectName("statusbar")
        MainWindowPortefeuille.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindowPortefeuille)
        self.toolBar.setObjectName("toolBar")
        MainWindowPortefeuille.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionClient = QtWidgets.QAction(MainWindowPortefeuille)
        self.actionClient.setEnabled(True)
        self.actionClient.setObjectName("actionClient")
        self.action_addClient = QtWidgets.QAction(MainWindowPortefeuille)
        self.action_addClient.setEnabled(True)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/ressources/img/icons8-add-user-male-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_addClient.setIcon(icon12)
        self.action_addClient.setObjectName("action_addClient")
        self.action_ficheClient = QtWidgets.QAction(MainWindowPortefeuille)
        self.action_ficheClient.setObjectName("action_ficheClient")
        self.actionPortefeuille = QtWidgets.QAction(MainWindowPortefeuille)
        self.actionPortefeuille.setObjectName("actionPortefeuille")
        self.action_deletePortefeuille = QtWidgets.QAction(MainWindowPortefeuille)
        self.action_deletePortefeuille.setIcon(icon10)
        self.action_deletePortefeuille.setObjectName("action_deletePortefeuille")
        self.action_modifyPortefeuilleName = QtWidgets.QAction(MainWindowPortefeuille)
        self.action_modifyPortefeuilleName.setIcon(icon9)
        self.action_modifyPortefeuilleName.setObjectName("action_modifyPortefeuilleName")
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindowPortefeuille)
        QtCore.QMetaObject.connectSlotsByName(MainWindowPortefeuille)

    def retranslateUi(self, MainWindowPortefeuille):
        _translate = QtCore.QCoreApplication.translate
        MainWindowPortefeuille.setWindowTitle(_translate("MainWindowPortefeuille", "Gestionnaire de portefeuille"))
        self.groupBox.setTitle(_translate("MainWindowPortefeuille", "Sélection du client et du portefeuille"))
        self.btn_unlockClient.setText(_translate("MainWindowPortefeuille", "UnLock"))
        self.label.setText(_translate("MainWindowPortefeuille", "Liste des clients existants :"))
        self.label_2.setText(_translate("MainWindowPortefeuille", "Liste de ses portefeuilles :"))
        self.btn_unlockPortefeuille.setText(_translate("MainWindowPortefeuille", "UnLock"))
        self.btn_chooseClient.setText(_translate("MainWindowPortefeuille", "Choisir"))
        self.btn_choosePortefeuille.setText(_translate("MainWindowPortefeuille", "Choisir"))
        self.btn_newPortefeuille.setText(_translate("MainWindowPortefeuille", "Nouveau portefeuille"))
        self.label_portefeuilleChoisi.setText(_translate("MainWindowPortefeuille", "Portefeuille choisi :"))
        self.label_4.setText(_translate("MainWindowPortefeuille", "Liquidité :"))
        self.btn_liquidite.setText(_translate("MainWindowPortefeuille", "Valider liquidité"))
        self.btn_today.setText(_translate("MainWindowPortefeuille", "Aujourd\'hui"))
        self.label_dateChoisie.setText(_translate("MainWindowPortefeuille", "Date choisie :"))
        self.btn_transfert.setText(_translate("MainWindowPortefeuille", "Transférer le portefeuille"))
        self.btn_import.setText(_translate("MainWindowPortefeuille", "Importation XLS"))
        self.btn_export.setText(_translate("MainWindowPortefeuille", "Exportation XLS"))
        self.label_nbLignes.setText(_translate("MainWindowPortefeuille", "Nombres de lignes"))
        self.groupBox_2.setTitle(_translate("MainWindowPortefeuille", "Configuration"))
        self.label_7.setText(_translate("MainWindowPortefeuille", "ISIN"))
        self.label_8.setText(_translate("MainWindowPortefeuille", "Nombre"))
        self.label_9.setText(_translate("MainWindowPortefeuille", "Prix d\'achat"))
        self.label_10.setText(_translate("MainWindowPortefeuille", "Dernière MAJ"))
        self.label_11.setText(_translate("MainWindowPortefeuille", "Nominal"))
        self.label_6.setText(_translate("MainWindowPortefeuille", "Valo"))
        self.label_12.setText(_translate("MainWindowPortefeuille", "Valo. Acqui"))
        self.btn_add.setText(_translate("MainWindowPortefeuille", "Ajouter la ligne"))
        self.btn_modif.setText(_translate("MainWindowPortefeuille", "Modifier la ligne"))
        self.btn_suppr.setText(_translate("MainWindowPortefeuille", "Supprimer la ligne"))
        self.btn_vis.setText(_translate("MainWindowPortefeuille", "Menu Visualisation"))
        self.toolBar.setWindowTitle(_translate("MainWindowPortefeuille", "toolBar"))
        self.actionClient.setText(_translate("MainWindowPortefeuille", "Client"))
        self.action_addClient.setText(_translate("MainWindowPortefeuille", "Ajouter un client"))
        self.action_ficheClient.setText(_translate("MainWindowPortefeuille", "Fiche Client"))
        self.actionPortefeuille.setText(_translate("MainWindowPortefeuille", "Portefeuille"))
        self.action_deletePortefeuille.setText(_translate("MainWindowPortefeuille", "Supprimer le portefeuille"))
        self.action_modifyPortefeuilleName.setText(_translate("MainWindowPortefeuille", "Modifier le nom du portefeuille"))
from Tools.calendarwidgetperso import CalendarWidgetPerso
import ressources_rc