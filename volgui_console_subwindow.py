from PyQt5.QtWidgets import QWidget,QMdiSubWindow
from PyQt5.QtCore import  pyqtSlot , QMetaObject, Qt, pyqtSignal, QThreadPool
from model import *
from ui_volgui_console_subwindow import Ui_ConsoleSubWindow
import sys, subprocess

from volgui_cmd import Cmd, CmdSignals
from volgui_mdiwindow import VolGuiMdiWindow

class VolGuiConsoleMdiWindow(Ui_ConsoleSubWindow,VolGuiMdiWindow):


    def __init__(self, dumpname, parent=None):

        #super(VolGuiConsoleMdiWindow,self).__init__(parent)
        VolGuiMdiWindow.__init__(self,dumpname,"Console",parent)
        Ui_ConsoleSubWindow.__init__(self)
        QMetaObject.connectSlotsByName(self)  
        self.threadpool = QThreadPool()

        self.consolWidget = QWidget()
        self.setupUi(self.consolWidget)
        self.cmdButton.clicked.connect(self.on_cmdButton_clicked)
        self.mdiWindowPending.emit(self.windowName,"Pending ...")


    def prepareWindow(self):
       
        
        self.addWidget(self.consolWidget) # fonction defined in VolGuiMdiWindow. It adds a widget on QMdiSubWindow (i.e. this window)
        self.mdiWindowReady.emit(self.windowName,"Window Ready")

    #@pyqtSlot()
    def on_cmdButton_clicked(self):
       
        if self.lineEdit.text().strip() == "":
            return
       
        command = self.lineEdit.text()
        cmd = Cmd(command.split())
        cmd.signals.resultCmdReady.connect(self.handleCmd)
        self.threadpool.start(cmd)
    
        self.cmdButton.setEnabled(False)
    
    def handleCmd(self,cmdResult):
        
        self.plainTextEdit.setPlainText(cmdResult)
        self.cmdButton.setEnabled(True)



