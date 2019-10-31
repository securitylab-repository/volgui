#-*- coding: latin_1 -*-
import sys, subprocess 
import json
from collections import namedtuple
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSignal, QThreadPool
import re
from volgui_cmd import * 

class GraphNode():

    """ classe qui represente un noeud d'un fichier dot."""


    def __init__(self,identifiant):

        self.id = identifiant
        self.columns = {}
        self.children = []
    
    def add_column(self, name, value):
        """ Ajoute un attribut avec sa valeur au noeud."""
        self.columns[name] = value

    def get_node_id(self):
        """ retourne l'identifiant du noeud de type Node[0-9]+"""

        return self.id

    def get_node_columns(self):

        return self.columns

    def add_node_child(self,child):

        self.children.append(child)

    def get_node_children(self):

        return self.children

class VolGuiPstreeModel(QObject):

    """ Cette classe retourne les donnees de la commande pstree au format .dot"""

    modelReady = pyqtSignal(name='modelReady')
    
    def __init__(self,dumpname):

        super(VolGuiPstreeModel,self).__init__()

        command = ['vol.py', '-f', dumpname ,'--profile=Win7SP1x86', 'pstree','--output=dot']
        self.threadpool = QThreadPool()
        
        cmd = Cmd(command)
        cmd.signals.resultReady.connect(self.builtModel)
        self.threadpool.start(cmd)

    def builtModel(self,pluginresult):


        nodes_line = re.findall(r'Node[0-9]+ \[.*];',pluginresult)
        
        self.nodes = {} # sauvegarde les noeuds resultant du parse 

        for node_line in nodes_line:

            node = re.findall(r'^(Node[0-9]+)',node_line)
            gnode = GraphNode(node[0])
    
            columns_line = re.findall(r'\{.*\}',node_line)
            columns_line = re.split('\|',columns_line[0].strip('{}'))
            for column in columns_line:
        
                col = re.split(':',column)
                gnode.add_column(col[0],col[1].strip())

            self.nodes[node[0]] = gnode


        arcs_ligne = re.findall(r'Node[0-9]+ -> *Node[0-9]+',pluginresult)

        for arc in arcs_ligne:

            result = re.split(r'->',arc)
            self.nodes[result[0].strip()].add_node_child(result[1].strip())

        self.modelReady.emit()


    def get_nodes(self):

        return self.nodes
