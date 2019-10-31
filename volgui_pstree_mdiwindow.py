from PyQt5.QtWidgets import QWidget,QMdiSubWindow,QVBoxLayout, QTabWidget,  QTreeView
from PyQt5.QtCore import  pyqtSlot , QMetaObject, pyqtSignal

import sys, subprocess

from volgui_cmd import Cmd, CmdSignals
from volgui_mdiwindow import VolGuiMdiWindow
from volgui_pstree_graph import *
from volgui_pstree_model import *
from model import Model

class VolGuiPstreeMdiWindow(VolGuiMdiWindow):


    def __init__(self,dumpname,parent=None):

        
        VolGuiMdiWindow.__init__(self,dumpname,"PSTREE",parent)
        QMetaObject.connectSlotsByName(self)  
        
        self.graph = None
        self.model = None

        self.tab_per_process = {}
        self.model_per_process_action = {}


    def prepareWindow(self):
        
        self.mdiWindowPending.emit(self.windowName,"Pending ....")

        self.model = VolGuiPstreeModel(self.dumpName)
        
        self.model.modelReady.connect(self.printWindow)

    def printWindow(self):
       
        self.graph  = GraphWidget(self.model,self)
        self.graph.CtxMenuActionClicked.connect(self.on_pstreeGraph_menuActionTriggered)

        self.addWidget(self.graph)
        self.mdiWindowReady.emit(self.windowName,"Window Ready")

    def hideWindow(self):

        self.graph.hide()
        self.hide()


    #action : dlllist, getsids, privs,... 
    #proc_columns : dict of process informations
    def on_pstreeGraph_menuActionTriggered(self,proc_columns,action):
        
        cmd = ['vol.py', '-f', self.dumpName ,'--profile=Win7SP1x86', action,'--output=json', '-p', str(proc_columns['Pid'])]
        self.model_per_process_action[proc_columns['Pid']+action] = Model(cmd,proc_columns,action)
        self.model_per_process_action[proc_columns['Pid']+action].modelReadyd.connect(self.printOngletProcess)



    #action : dlllist, getsids, privs,... 
    # process : list of process informations
    def printOngletProcess(self,process,action):
       
        if process['Pid'] in self.tab_per_process :

            tabs_widget = self.tab_per_process[process['Pid']][0]
            tabs = self.tab_per_process[process['Pid']][1]
            vLayout_tabs =  self.tab_per_process[process['Pid']][2]

        else:

            print(process['Pid'])
            tabs_widget = QWidget()
            tabs_widget.setWindowTitle("{0}[{1}]".format(process['Name'],process['Pid']))
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
        treeView.setModel(self.model_per_process_action[process['Pid']+action])
        vLayout_tabs.addWidget(treeView)
        tabs.addTab(treeView, "%s"%action)
        tabs.setCurrentWidget(treeView)
        
        if  process['Pid'] not in self.tab_per_process.keys():
            self.tab_per_process[process['Pid']] = [ tabs_widget,tabs,vLayout_tabs ]
            self.newMdiWindowAdded.emit(tabs_widget)

        
        tabs_widget.show()





       
