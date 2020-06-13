# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FindISIN.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogFindISIN(object):
    def setupUi(self, DialogFindISIN):
        DialogFindISIN.setObjectName("DialogFindISIN")
        DialogFindISIN.resize(377, 202)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogFindISIN)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(DialogFindISIN)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.tb_ISIN = QtWidgets.QLineEdit(DialogFindISIN)
        self.tb_ISIN.setReadOnly(False)
        self.tb_ISIN.setObjectName("tb_ISIN")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tb_ISIN)
        self.label_2 = QtWidgets.QLabel(DialogFindISIN)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.tb_libelle = QtWidgets.QLineEdit(DialogFindISIN)
        self.tb_libelle.setObjectName("tb_libelle")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.tb_libelle)
        self.verticalLayout.addLayout(self.formLayout)
        self.listWidget = QtWidgets.QListWidget(DialogFindISIN)
        self.listWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogFindISIN)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogFindISIN)
        self.buttonBox.accepted.connect(DialogFindISIN.accept)
        self.buttonBox.rejected.connect(DialogFindISIN.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogFindISIN)

    def retranslateUi(self, DialogFindISIN):
        _translate = QtCore.QCoreApplication.translate
        DialogFindISIN.setWindowTitle(_translate("DialogFindISIN", "Création de portefeuille"))
        self.label.setText(_translate("DialogFindISIN", "ISIN"))
        self.label_2.setText(_translate("DialogFindISIN", "Libellé"))

