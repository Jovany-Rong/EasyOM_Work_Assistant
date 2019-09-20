# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/jovany_rong/dev/python3/EasyOM_Work_Assistant/UIs/addEmer.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_addEmer(object):
    def setupUi(self, addEmer):
        addEmer.setObjectName("addEmer")
        addEmer.resize(640, 240)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(addEmer)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.taskNameLabel = QtWidgets.QLabel(addEmer)
        self.taskNameLabel.setMinimumSize(QtCore.QSize(0, 20))
        self.taskNameLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.taskNameLabel.setObjectName("taskNameLabel")
        self.verticalLayout.addWidget(self.taskNameLabel)
        self.taskName = QtWidgets.QLineEdit(addEmer)
        self.taskName.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.taskName.setObjectName("taskName")
        self.verticalLayout.addWidget(self.taskName)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.taskTimeLabel = QtWidgets.QLabel(addEmer)
        self.taskTimeLabel.setMinimumSize(QtCore.QSize(0, 20))
        self.taskTimeLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.taskTimeLabel.setObjectName("taskTimeLabel")
        self.verticalLayout_2.addWidget(self.taskTimeLabel)
        self.taskTime = QtWidgets.QDateTimeEdit(addEmer)
        self.taskTime.setObjectName("taskTime")
        self.verticalLayout_2.addWidget(self.taskTime)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.taskSolutionLabel = QtWidgets.QLabel(addEmer)
        self.taskSolutionLabel.setMinimumSize(QtCore.QSize(0, 20))
        self.taskSolutionLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.taskSolutionLabel.setObjectName("taskSolutionLabel")
        self.verticalLayout_3.addWidget(self.taskSolutionLabel)
        self.taskSolution = QtWidgets.QTextEdit(addEmer)
        self.taskSolution.setObjectName("taskSolution")
        self.verticalLayout_3.addWidget(self.taskSolution)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.okButton = QtWidgets.QPushButton(addEmer)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_2.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(addEmer)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.horizontalLayout_2.setStretch(0, 6)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(addEmer)
        QtCore.QMetaObject.connectSlotsByName(addEmer)

    def retranslateUi(self, addEmer):
        _translate = QtCore.QCoreApplication.translate
        addEmer.setWindowTitle(_translate("addEmer", "Emergency Add"))
        self.taskNameLabel.setText(_translate("addEmer", "<html><head/><body><p>task name</p></body></html>"))
        self.taskTimeLabel.setText(_translate("addEmer", "<html><head/><body><p>task time</p></body></html>"))
        self.taskSolutionLabel.setText(_translate("addEmer", "<html><head/><body><p>task solution</p></body></html>"))
        self.okButton.setText(_translate("addEmer", "确定"))
        self.cancelButton.setText(_translate("addEmer", "取消"))

