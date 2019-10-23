# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/jovany_rong/dev/python3/EasyOM_Work_Assistant/UIs/deliCommit.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DeliCommit(object):
    def setupUi(self, DeliCommit):
        DeliCommit.setObjectName("DeliCommit")
        DeliCommit.resize(640, 92)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(DeliCommit)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(DeliCommit)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.deli = QtWidgets.QLineEdit(DeliCommit)
        self.deli.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.deli.setObjectName("deli")
        self.verticalLayout.addWidget(self.deli)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.okButton = QtWidgets.QPushButton(DeliCommit)
        self.okButton.setObjectName("okButton")
        self.verticalLayout_2.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(DeliCommit)
        self.cancelButton.setObjectName("cancelButton")
        self.verticalLayout_2.addWidget(self.cancelButton)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(DeliCommit)
        QtCore.QMetaObject.connectSlotsByName(DeliCommit)

    def retranslateUi(self, DeliCommit):
        _translate = QtCore.QCoreApplication.translate
        DeliCommit.setWindowTitle(_translate("DeliCommit", "提交可交付成果"))
        self.label.setText(_translate("DeliCommit", "<html><head/><body><p>请输入可交付成果（SVN地址、禅道地址或其他描述等形式）</p></body></html>"))
        self.okButton.setText(_translate("DeliCommit", "确定"))
        self.cancelButton.setText(_translate("DeliCommit", "取消"))

