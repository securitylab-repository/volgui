from PyQt5.QtWidgets import QProgressDialog, QWidget
from PyQt5.QtCore import  pyqtSlot , QMetaObject,  QTimer


class VolGuiProgressDialog(QProgressDialog):

    def __init__(self,widget):

        super(VolGuiProgressDialog,self).__init__("Operation in progress.","Cancel", 0 ,100)
        self.canceled.connect(self.progressCancel)
        self.setMinimumDuration(1000)
        self.timer = QTimer(widget)
        self.step = 1
        self.timer.timeout.connect(self.progress)
        self.timer.start(1000)

    def progress(self):

        self.setValue(self.step)
        self.step = self.step + 1  
        if (self.step > self.maximum()):
            self.timer.stop()

    def progressCancel(self):

        self.timer.stop()
