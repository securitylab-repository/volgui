#-*- coding: latin_1 -*-
import sys, subprocess 
import json
from collections import namedtuple
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QObject, pyqtSlot , QMetaObject, pyqtSignal, QThreadPool

from volgui_cmd import *

"""
    Import this module if you want to interpret the volatility command results 
"""


class Model(QAbstractTableModel):

    """
    Model that parses results of a  volatility command 
    """

    modelReadyd = pyqtSignal(dict,'QString',name='modelReadyd')
    modelReadyl = pyqtSignal(list,'QString',name='modelReadyl')

    def __init__(self, command, proc , cmd_name=""):
        
        """ Constructor

        :param command : related volatility
        :param proc : process informations, can be list or dict
        
        """
        super(Model,self).__init__()
        self.proc_info = proc
        self.cmd_name = cmd_name
        self.command = command
        self.titresColonnes = []        
        self.objet_type = None
        self.objets  = []
        self.threadpool = QThreadPool()
        
        cmd = Cmd(command)
        cmd.signals.resultReady.connect(self.builtModel)
        self.threadpool.start(cmd)

    def builtModel(self,cmdResult):

        elt_level1 = json.loads(cmdResult)
        self.titresColonnes = elt_level1['columns'][1:]
        self.objet_type = namedtuple ('objet_type',elt_level1['columns'][1:])
        self.objets = [self.objet_type(*row[1:]) for row in elt_level1['rows'][1:]]
        
        if(isinstance(self.proc_info,dict)):
            self.modelReadyd.emit(self.proc_info,self.cmd_name)
        else:
            self.modelReadyl.emit(self.proc_info,self.cmd_name)


    def headerData(self,section,orientation,role):

        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.titresColonnes[section]

        return QVariant()

    def columnCount(self,parent):

        return len(self.titresColonnes)

    def rowCount(self,parent):
        return len(self.objets)

    def data(self,index,role):

        if role == Qt.DisplayRole and index.isValid():

            return (self.objets[index.row()][index.column()])
        return QVariant()





