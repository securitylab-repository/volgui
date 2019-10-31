#-*- coding: latin_1 -*-
import sys, subprocess 
from PyQt5.QtCore import QObject,  pyqtSlot , QMetaObject, pyqtSignal, QRunnable, QThreadPool

class CmdSignals(QObject):

    '''
    signals that can be sent by Cmd class
    '''

    resultCmdReady = pyqtSignal(['QString'],name='resultReady') 


class Cmd(QRunnable):
    '''
    task that creates a model of a volatility command
    '''

    def __init__(self,command):

        super(Cmd,self).__init__()
        self.signals = CmdSignals() # use it like this : cmdobjet.signals.resultCmdReady.connect(method)
        self.command = command
    
    @pyqtSlot()
    def run(self):

        p = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmdResult, err = p.communicate()

        if cmdResult:
            self.signals.resultCmdReady.emit(cmdResult.decode('utf-8'))



