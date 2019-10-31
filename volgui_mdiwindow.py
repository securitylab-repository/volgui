# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import  QObject, pyqtSlot , QMetaObject, pyqtSignal , Qt 


#todo
# rendre cette classe singleton
class VolGuiMdiWindow(QMdiSubWindow,QObject):
    '''
    Base class for Mdi Windows to add as plugins or not to volgui main interface 
    
    '''

    newMdiWindowAdded = pyqtSignal('QWidget',name='newMdiWindowAdded') # signal is sent when new window is created from this window
    
    mdiWindowClosed = pyqtSignal(name='mdiWindowClosed') # signal is sent when the window is closed

    # pyqtSignal(window_name,message,signal_name)
    mdiWindowPending = pyqtSignal('QString','QString',name='mdiWindowPending') 
    mdiWindowReady = pyqtSignal('QString','QString',name='mdiWindowReady') # signal is sent when this window is ready


    def __init__(self,dumpname, winname=None, parent=None):

        super(VolGuiMdiWindow,self).__init__() # adding a parent (ceci affiche la barre de la fenêtre en attendant son affichage complet

        QMetaObject.connectSlotsByName(self)  
        
        self.dumpName = dumpname # name of a memory dump to analyse 

        self.windowName = winname # the name of MdiWindow
        
        self.setWindowTitle(winname)

        self.mdiWindowReady.connect(parent.addLog)
        self.mdiWindowPending.connect(parent.addLog)

    def addWidget(self,widget):
        
        self.setWidget(widget)
        widget.show()
    
    def prepareWindow(self):
        '''
        This fucntion must be overridden.
        It is called by the volgui main interface.
        You must add here the necessary code that prepare and/or print the subclass window of this class, 
        and signals, to the volgui main interface, the end of the preparing or prting by using mdiWindoReady signal.
        '''
        return

    def closeEvent(self,event):
        
        self.mdiWindowClosed.emit()
        event.accept()


