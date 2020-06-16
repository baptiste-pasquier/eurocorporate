# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ModifyPortefeuille.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogModifyPortefeuille(object):
    def setupUi(self, DialogModifyPortefeuille):
        DialogModifyPortefeuille.setObjectName("DialogModifyPortefeuille")
        DialogModifyPortefeuille.resize(377, 202)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/icone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogModifyPortefeuille.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogModifyPortefeuille)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(DialogModifyPortefeuille)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.tb_client = QtWidgets.QLineEdit(DialogModifyPortefeuille)
        self.tb_client.setReadOnly(True)
        self.tb_client.setObjectName("tb_client")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tb_client)
        self.label_2 = QtWidgets.QLabel(DialogModifyPortefeuille)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.tb_ancienLibelle = QtWidgets.QLineEdit(DialogModifyPortefeuille)
        self.tb_ancienLibelle.setReadOnly(True)
        self.tb_ancienLibelle.setObjectName("tb_ancienLibelle")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.tb_ancienLibelle)
        self.label_3 = QtWidgets.QLabel(DialogModifyPortefeuille)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.tb_nouvLibelle = QtWidgets.QLineEdit(DialogModifyPortefeuille)
        self.tb_nouvLibelle.setObjectName("tb_nouvLibelle")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.tb_nouvLibelle)
        self.verticalLayout.addLayout(self.formLayout)
        self.tb_message = QtWidgets.QTextEdit(DialogModifyPortefeuille)
        self.tb_message.setReadOnly(True)
        self.tb_message.setObjectName("tb_message")
        self.verticalLayout.addWidget(self.tb_message)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogModifyPortefeuille)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogModifyPortefeuille)
        self.buttonBox.accepted.connect(DialogModifyPortefeuille.accept)
        self.buttonBox.rejected.connect(DialogModifyPortefeuille.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogModifyPortefeuille)

    def retranslateUi(self, DialogModifyPortefeuille):
        _translate = QtCore.QCoreApplication.translate
        DialogModifyPortefeuille.setWindowTitle(_translate("DialogModifyPortefeuille", "Modification de portefeuille"))
        self.label.setText(_translate("DialogModifyPortefeuille", "Client"))
        self.label_2.setText(_translate("DialogModifyPortefeuille", "Ancien libellé"))
        self.label_3.setText(_translate("DialogModifyPortefeuille", "Nouveau libellé"))

import ressources_rc
