# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'volgui_mainwin.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(915, 621)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mdi = QtWidgets.QMdiArea(self.centralwidget)
        self.mdi.setTabsClosable(True)
        self.mdi.setObjectName("mdi")
        self.verticalLayout.addWidget(self.mdi)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 915, 19))
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        self.menu_Affichage = QtWidgets.QMenu(self.menubar)
        self.menu_Affichage.setObjectName("menu_Affichage")
        self.menu_Aide = QtWidgets.QMenu(self.menubar)
        self.menu_Aide.setObjectName("menu_Aide")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionEnregistrer = QtWidgets.QAction(MainWindow)
        self.actionEnregistrer.setObjectName("actionEnregistrer")
        self.actionNouveau = QtWidgets.QAction(MainWindow)
        self.actionNouveau.setObjectName("actionNouveau")
        self.action_tz = QtWidgets.QAction(MainWindow)
        self.action_tz.setObjectName("action_tz")
        self.action_Enregistrer = QtWidgets.QAction(MainWindow)
        self.action_Enregistrer.setEnabled(False)
        self.action_Enregistrer.setObjectName("action_Enregistrer")
        self.action_Quitter = QtWidgets.QAction(MainWindow)
        self.action_Quitter.setObjectName("action_Quitter")
        self.action_Quitter_2 = QtWidgets.QAction(MainWindow)
        self.action_Quitter_2.setObjectName("action_Quitter_2")
        self.action_Ouvrir = QtWidgets.QAction(MainWindow)
        self.action_Ouvrir.setObjectName("action_Ouvrir")
        self.action_Console = QtWidgets.QAction(MainWindow)
        self.action_Console.setCheckable(False)
        self.action_Console.setEnabled(False)
        self.action_Console.setObjectName("action_Console")
        self.action_Pslist = QtWidgets.QAction(MainWindow)
        self.action_Pslist.setCheckable(True)
        self.action_Pslist.setEnabled(False)
        self.action_Pslist.setObjectName("action_Pslist")
        self.action_Pstree_Graph = QtWidgets.QAction(MainWindow)
        self.action_Pstree_Graph.setCheckable(True)
        self.action_Pstree_Graph.setEnabled(False)
        self.action_Pstree_Graph.setObjectName("action_Pstree_Graph")
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.action_Ouvrir)
        self.menuFichier.addAction(self.action_Enregistrer)
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.action_Quitter_2)
        self.menu_Affichage.addAction(self.action_Console)
        self.menu_Affichage.addAction(self.action_Pslist)
        self.menu_Affichage.addAction(self.action_Pstree_Graph)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menu_Affichage.menuAction())
        self.menubar.addAction(self.menu_Aide.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VolGui"))
        self.menuFichier.setTitle(_translate("MainWindow", "&Fichier"))
        self.menu_Affichage.setTitle(_translate("MainWindow", "&Affichage"))
        self.menu_Aide.setTitle(_translate("MainWindow", "A&ide"))
        self.actionEnregistrer.setText(_translate("MainWindow", "Enregistrer"))
        self.actionEnregistrer.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionNouveau.setText(_translate("MainWindow", "Nouveau"))
        self.action_tz.setText(_translate("MainWindow", "&tz"))
        self.action_Enregistrer.setText(_translate("MainWindow", "&Enregistrer"))
        self.action_Enregistrer.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.action_Quitter.setText(_translate("MainWindow", "&Quitter"))
        self.action_Quitter_2.setText(_translate("MainWindow", "&Quitter"))
        self.action_Quitter_2.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.action_Ouvrir.setText(_translate("MainWindow", "&Ouvrir"))
        self.action_Ouvrir.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_Console.setText(_translate("MainWindow", "&Console"))
        self.action_Console.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.action_Pslist.setText(_translate("MainWindow", "&Pslist"))
        self.action_Pslist.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.action_Pstree_Graph.setText(_translate("MainWindow", "&Pstree Graph"))
        self.action_Pstree_Graph.setShortcut(_translate("MainWindow", "Ctrl+G"))

