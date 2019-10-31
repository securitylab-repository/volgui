# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTreeView, QWidget,QMessageBox, QMenu,QAction
from PyQt5.QtCore import  pyqtSlot , QMetaObject, Qt, pyqtSignal
from model import *

class VolGuiPslistTreeView(QTreeView):
    '''
        subclass  QTreeView to manage pslist volgui command result
    '''
    
    menuActionClicked = pyqtSignal(list,'QString',name='menuActionClicked')

    def __init__(self,parent,model):

        super(VolGuiPslistTreeView,self).__init__(parent)
        QMetaObject.connectSlotsByName(self)  
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openContextMenu) # widget class signal
        self.model = model
        self.setModel(self.model) 
    
    def openContextMenu(self, position):
        
        menu = QMenu()
        menu.triggered.connect(self.qmenuActionTriggered)
        

        menu.addAction("dlllist")
        menu.addAction("getsids")
        menu.addAction("privs")
        menu.addAction("handles")

        menu.exec_(self.viewport().mapToGlobal(position))
    

    def qmenuActionTriggered(self,action):
        
        indexes = self.selectedIndexes()
        
        if len(indexes) > 0:

            indexSelection = indexes[0]
            print(indexSelection.row())
            self.menuActionClicked.emit([self.model.objets[indexSelection.row()]],action.text())

            
       
