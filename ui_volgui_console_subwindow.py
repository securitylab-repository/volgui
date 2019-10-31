# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'volgui_console_subwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConsoleSubWindow(object):
    def setupUi(self, ConsoleSubWindow):
        ConsoleSubWindow.setObjectName("ConsoleSubWindow")
        ConsoleSubWindow.resize(783, 535)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConsoleSubWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(ConsoleSubWindow)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(ConsoleSubWindow)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.cmdButton = QtWidgets.QPushButton(ConsoleSubWindow)
        self.cmdButton.setObjectName("cmdButton")
        self.horizontalLayout.addWidget(self.cmdButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ConsoleSubWindow)
        QtCore.QMetaObject.connectSlotsByName(ConsoleSubWindow)

    def retranslateUi(self, ConsoleSubWindow):
        _translate = QtCore.QCoreApplication.translate
        ConsoleSubWindow.setWindowTitle(_translate("ConsoleSubWindow", "Console"))
        self.cmdButton.setText(_translate("ConsoleSubWindow", ">"))

