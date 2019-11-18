# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QMessageBox, QMdiSubWindow, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, QMetaObject, Qt, QThread

from ui_volgui_mainwin import Ui_MainWindow
from volgui_console_subwindow import VolGuiConsoleMdiWindow
from volgui_pslist_mdiwindow import VolGuiPslistMdiWindow
from volgui_pstree_graph import *
from volgui_pstree_mdiwindow import VolGuiPstreeMdiWindow
from volgui_cmd import *;

import subprocess
from volgui_profile import *

class VolGuiMainWindow(QMainWindow, Ui_MainWindow):

    """VolGuiMainWindow inherits from Ui_MainWindow

    :param   Ui_MainWindow : generated with QtDesigner

    """

    def __init__(self, parent=None):

        super(VolGuiMainWindow, self).__init__(parent)
        self.setupUi(self)
        QMetaObject.connectSlotsByName(self)

        self.dumpname = None  # the name of a dump file to analyse

        self.console = None
        self.pslistWindow = None
        self.pstreeWindow = None

        self.close_cpt = 0
        # self.action_Ouvrir.triggered.connect(self.on_action_Ouvrir_triggered)

    ##################################################################################################
    # manage the submenu File --> Open or fichier -> ouvrir
    #################################################################################################
    @pyqtSlot()
    def on_action_Ouvrir_triggered(self):

        """
            Click on  File --> Open event handler
            
        """

        if self.dumpname is None:

            #  self.dumpname, _ = QFileDialog.getOpenFileName(self,"Ouvrir un fichier dump","/home/debian")
            dumpname = None
            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.ExistingFile)
            if dlg.exec_():
                dumpname = dlg.selectedFiles()[0]

            if dumpname is not None:

                self.dumpname = dumpname

                # build image profile
                command = ['vol.py', '-f', self.dumpname, 'imageinfo', '--output=json']
                p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                cmd_result, err = p.communicate()

                if cmd_result:
                    self.profile = Profile()
                    self.profile.build_profile(cmd_result.decode('utf-8'))

                self.action_Pslist.setEnabled(True)
                self.action_Console.setEnabled(True)
                self.action_Pstree_Graph.setEnabled(True)


    #######################################################################################################
    # Gestion de la fenetre PSLIST
    ######################################################################################################

    @pyqtSlot()
    def on_action_Pslist_triggered(self):

        if self.action_Pslist.isChecked():

            self.pslist()

        else:

            self.pslistWindow.hide()
            self.mdi.tileSubWindows()

    def pslist(self):

        if not self.pslistWindow:

            self.pslistWindow = VolGuiPslistMdiWindow(self.dumpname, self)
            self.pslistWindow.mdiWindowClosed.connect(self.pslistWindowClosed)
            self.pslistWindow.mdiWindowReady.connect(self.pslistWindowReady)
            self.pslistWindow.newMdiWindowAdded.connect(self.on_newMdiWindow)
            self.pslistWindow.prepareWindow()
        else:

            self.updatePslistWindow()

    def updatePslistWindow(self):

        self.pslistWindow.show()
        self.mdi.tileSubWindows()

    def pslistWindowClosed(self):

        self.action_Pslist.setChecked(False)
        self.pslistWindow = None
        self.mdi.tileSubWindows()

    def pslistWindowReady(self, winame):

        self.mdi.addSubWindow(self.pslistWindow)
        self.pslistWindow.show()
        self.mdi.tileSubWindows()

    #######################################################################################################################
    # Gestion de la fermeture de l'application
    ######################################################################################################################

    def closeEvent(self, event):

        #    if self.close_cpt == 0:
        messageConfirmation = "Are you closing application ?"
        reponse = QMessageBox.question(self, "Confirmation", messageConfirmation, QMessageBox.Yes, QMessageBox.No)
        #       self.close_cpt = self.close_cpt + 1

        if reponse == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    #  else:
    #     event.ignore()

    @pyqtSlot()
    def on_action_Quitter_2_triggered(self):
        self.close()

    ##########################################################################################################################
    # Gestion de la console
    #########################################################################################################################

    @pyqtSlot()
    def on_action_Console_triggered(self):

        if not self.console:

            self.console = VolGuiConsoleMdiWindow(self.dumpname, self)
            self.console.mdiWindowClosed.connect(self.consoleWindowClosed)
            self.console.mdiWindowReady.connect(self.consoleWindowReady)
            self.console.prepareWindow()

        else:
            self.updateConsole()

    def updateConsole(self):

        self.console.show()
        self.mdi.tileSubWindows()

    def consoleWindowReady(self, winname):

        self.mdi.addSubWindow(self.console)
        self.console.show()
        self.mdi.tileSubWindows()

    def consoleWindowClosed(self):

        self.console = None
        self.mdi.tileSubWindows()

    ##########################################################################################################################
    # Gestion du graphe pstree
    #########################################################################################################################

    @pyqtSlot()
    def on_action_Pstree_Graph_triggered(self):

        if self.action_Pstree_Graph.isChecked():
            self.pstree()
        else:

            self.pstreeWindow.hide()
            self.mdi.tileSubWindows()

    def pstree(self):

        if not self.pstreeWindow:

            self.pstreeWindow = VolGuiPstreeMdiWindow(self.dumpname, self)
            self.pstreeWindow.mdiWindowClosed.connect(self.pstreeWindowClosed)
            self.pstreeWindow.mdiWindowReady.connect(self.pstreeWindowReady)
            self.pstreeWindow.newMdiWindowAdded.connect(self.on_newMdiWindow)
            self.pstreeWindow.prepareWindow()

        else:
            self.updatePstreeWindow()

    def updatePstreeWindow(self):

        self.pstreeWindow.show()
        self.mdi.tileSubWindows()

    def pstreeWindowReady(self, winname):

        self.mdi.addSubWindow(self.pstreeWindow)
        self.pstreeWindow.show()
        self.mdi.tileSubWindows()

    def pstreeWindowClosed(self):

        self.action_Pstree_Graph.setChecked(False)
        self.pstreeWindow = None
        self.mdi.tileSubWindows()

    ##########################################################################################################################
    # Gestion des Logs
    #########################################################################################################################

    def addLog(self, winname, message):

        print("Window Name: {0}     Message: {1}".format(winname, message))

    ############################################################################################################################
    # For All
    ############################################################################################################################

    def on_newMdiWindow(self, window):

        self.mdi.addSubWindow(window)
        window.show()
        self.mdi.tileSubWindows()
