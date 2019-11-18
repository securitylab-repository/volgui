# -*- coding: latin_1 -*-
import subprocess

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QRunnable


class CmdSignals(QObject):
    """
    Signals that can be sent by Cmd class

    """
    resultCmdReady = pyqtSignal(['QString'], name='resultReady')


class Cmd(QRunnable):
    """
    Task that creates a model of a volatility command

    """

    def __init__(self, command):
        super(Cmd, self).__init__()
        self.signals = CmdSignals()  # use it like this : cmdobjet.signals.resultCmdReady.connect(method)
        self.command = command

    @pyqtSlot()
    def run(self):
        p = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmdResult, err = p.communicate()

        if cmdResult:
            self.signals.resultCmdReady.emit(cmdResult.decode('utf-8'))

            
