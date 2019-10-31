# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTreeView, QWidget, QVBoxLayout, QTabWidget, QMdiSubWindow,QMessageBox
from PyQt5.QtCore import  QObject, pyqtSlot , QMetaObject, Qt, pyqtSignal, QAbstractTableModel,QRunnable, QThreadPool,QMutex 

from model import Model
from volgui_pslist_treeview import VolGuiPslistTreeView 
from volgui_mdiwindow import VolGuiMdiWindow


class VolGuiPslistMdiWindow(VolGuiMdiWindow):


    def __init__(self,dumpname, parent=None):

        super(VolGuiPslistMdiWindow,self).__init__(dumpname,"PSLIST",parent)
        QMetaObject.connectSlotsByName(self)  
        
        self.tab_per_process = {}
        self.model_per_process_action = {}
    
    def prepareWindow(self):
        
        self.mdiWindowPending.emit(self.windowName,"Pending ....")

        cmd = ['vol.py', '-f', self.dumpName ,'--profile=Win7SP1x86', 'pslist','--output=json']
        self.modelPslist = Model(cmd,[])
        self.modelPslist.modelReadyl.connect(self.printWindow)

    def printWindow(self,proc,cmd_name):

        self.pslistWidget = QWidget()
        self.pslistTreeView = VolGuiPslistTreeView(self.pslistWidget,self.modelPslist)

        verticalLayout = QVBoxLayout(self.pslistWidget)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
                
        verticalLayout.addWidget(self.pslistTreeView)
        
        self.pslistTreeView.menuActionClicked.connect(self.on_pslistTreeView_menuActionTriggered)

        self.addWidget(self.pslistWidget)
        
        self.mdiWindowReady.emit(self.windowName,"Window Ready")
        
    
    def hideWindow(self):

        self.pslistWidget.hide()
        self.hide()
        
    def closeEvent(self,event):
        
        self.mdiWindowClosed.emit()
        event.accept()


################################################################################################################################
# Gestion des onglets par processus
###############################################################################################################################
        
    def on_pslistTreeView_menuActionTriggered(self,process,action):
        
        if (str(process[0].PID)+action in self.model_per_process_action):
            
            return
       
        cmd = ['vol.py', '-f', self.dumpName ,'--profile=Win7SP1x86', action,'--output=json', '-p', str(process[0].PID)]
        self.model_per_process_action[str(process[0].PID)+action] = Model(cmd,process,action)
        self.model_per_process_action[str(process[0].PID)+action].modelReadyl.connect(self.printOngletProcess)
        
    
    def printOngletProcess(self,process,action):
        

        if str(process[0].PID) in self.tab_per_process :
            
            tabs_widget = self.tab_per_process[str(process[0].PID)][0]
            tabs = self.tab_per_process[str(process[0].PID)][1]
            vLayout_tabs =  self.tab_per_process[str(process[0].PID)][2]

        else:
            
            tabs_widget = QWidget()
            tabs_widget.setWindowTitle("{0}[{1}]".format(process[0].Name,str(process[0].PID)))
            vLayout_tabs_widget = QVBoxLayout(tabs_widget)
            vLayout_tabs_widget.setContentsMargins(0, 0, 0, 0)

            tabs = QTabWidget(tabs_widget)
            vLayout_tabs = QVBoxLayout(tabs)
            vLayout_tabs.setContentsMargins(0, 0, 0, 0)
            tabs.setEnabled(True)
            tabs.setAcceptDrops(False)
            tabs.setTabsClosable(True)
            vLayout_tabs_widget.addWidget(tabs)
        
        treeView = QTreeView(tabs)
        treeView.setModel(self.model_per_process_action[str(process[0].PID)+action])
        vLayout_tabs.addWidget(treeView)
        tabs.addTab(treeView, "%s"%action)
        tabs.setCurrentWidget(treeView)
        
        if  str(process[0].PID) not in self.tab_per_process.keys():
            self.tab_per_process[str(process[0].PID)] = [ tabs_widget,tabs,vLayout_tabs ]
            self.newMdiWindowAdded.emit(tabs_widget)
        
        tabs_widget.show()

    
