# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddPortefeuille.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogAddPortefeuille(object):
    def setupUi(self, DialogAddPortefeuille):
        DialogAddPortefeuille.setObjectName("DialogAddPortefeuille")
        DialogAddPortefeuille.resize(377, 202)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/icone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogAddPortefeuille.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogAddPortefeuille)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(DialogAddPortefeuille)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.tb_client = QtWidgets.QLineEdit(DialogAddPortefeuille)
        self.tb_client.setReadOnly(True)
        self.tb_client.setObjectName("tb_client")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tb_client)
        self.label_2 = QtWidgets.QLabel(DialogAddPortefeuille)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.tb_libelle = QtWidgets.QLineEdit(DialogAddPortefeuille)
        self.tb_libelle.setObjectName("tb_libelle")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.tb_libelle)
        self.verticalLayout.addLayout(self.formLayout)
        self.tb_message = QtWidgets.QTextEdit(DialogAddPortefeuille)
        self.tb_message.setReadOnly(True)
        self.tb_message.setObjectName("tb_message")
        self.verticalLayout.addWidget(self.tb_message)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogAddPortefeuille)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogAddPortefeuille)
        self.buttonBox.accepted.connect(DialogAddPortefeuille.accept)
        self.buttonBox.rejected.connect(DialogAddPortefeuille.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogAddPortefeuille)

    def retranslateUi(self, DialogAddPortefeuille):
        _translate = QtCore.QCoreApplication.translate
        DialogAddPortefeuille.setWindowTitle(_translate("DialogAddPortefeuille", "Création de portefeuille"))
        self.label.setText(_translate("DialogAddPortefeuille", "Client"))
        self.label_2.setText(_translate("DialogAddPortefeuille", "Libellé"))

import ressources_rc
