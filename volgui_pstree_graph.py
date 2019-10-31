import math

from PyQt5.QtCore import (qAbs, QLineF, QPointF, qrand, QRectF, QSizeF, qsrand,
        Qt, QTime,pyqtSignal )
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPainter,
        QPainterPath, QPen, QPolygonF, QRadialGradient)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsScene,
        QGraphicsView, QStyle, QMenu,QGraphicsProxyWidget)

from volgui_pstree_model import *


class Edge(QGraphicsItem):

    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        super(Edge, self).__init__()

        self.arrowSize = 10.0
        self.sourcePoint = QPointF()
        self.destPoint = QPointF()

        self.setAcceptedMouseButtons(Qt.NoButton)
        self.source = sourceNode
        self.dest = destNode
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.adjust()

    def type(self):
        return Edge.Type

    def sourceNode(self):
        return self.source

    def setSourceNode(self, node):
        self.source = node
        self.adjust()

    def destNode(self):
        return self.dest

    def setDestNode(self, node):
        self.dest = node
        self.adjust()

    def adjust(self):
        if not self.source or not self.dest:
            return
        
        line = QLineF(self.mapFromItem(self.source, 0, 0),self.mapFromItem(self.dest, 0, 0))
        length = line.length()
       
        self.prepareGeometryChange()
        
        self.sourcePoint = line.p1()
        self.destPoint = line.p2()
        

    def boundingRect(self):


        if not self.source or not self.dest:
            return QRectF()

        #penWidth = 1.0
        #extra = (penWidth + self.arrowSize) / 2.0
        return QRectF(self.sourcePoint ,QSizeF(self.destPoint.x() - self.sourcePoint.x(), (self.destPoint.y() - self.sourcePoint.y())))

        #return QRectF(self.sourcePoint,
         #       QSizeF(self.destPoint.x() - self.sourcePoint.x(),
          #              self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        if not self.source or not self.dest:
            return

        # Draw the line itself.
        line = QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap,Qt.RoundJoin))
        painter.drawLine(line)

        # Draw the arrows if there's enough room.
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = Edge.TwoPi - angle

        #sourceArrowP1 = self.sourcePoint + QPointF(math.sin(angle + Edge.Pi / 3) * self.arrowSize,
        #                                                  math.cos(angle + Edge.Pi / 3) * self.arrowSize)
        #sourceArrowP2 = self.sourcePoint + QPointF(math.sin(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize,
        #                                                  math.cos(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize);   
        destArrowP1 = self.destPoint + QPointF(math.sin(angle - Edge.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - Edge.Pi / 3) * self.arrowSize)
        destArrowP2 = self.destPoint + QPointF(math.sin(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize)

        painter.setBrush(Qt.black)
        #painter.drawPolygon(QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
        painter.drawPolygon(QPolygonF([line.p2(), destArrowP1, destArrowP2]))


class Node(QGraphicsItem):
    Type = QGraphicsItem.UserType + 1
    def __init__(self, graphWidget,x,y,columns,ctxmenusignal):
        super(Node, self).__init__()

        self.ctxmenusignal = ctxmenusignal

        self.columns = columns # It is a dictionnary of attributes (by model) names / values  
        self.x = 0 # origin 
        self.y = 0 # origin
        
        self.pos_x = x # x relatively to origin
        self.pos_y = y # y relatively to origin

        self.graph = graphWidget # reference to QGraphicsView object that includes this node
        self.edgeList = [] # list of edges starting from this node
        

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(1)

    def type(self):
        return Node.Type

    def addEdge(self, edge):
        self.edgeList.append(edge)
        edge.adjust()

    def edges(self):
        return self.edgeList

    
    def boundingRect(self):

        return QRectF(self.x,self.y,len(self.columns['Name'])*10,50)

    def paint(self, painter, option, widget):
        
        rect = self.boundingRect()
        #painter.drawRect(0, 0, 20, 20)

        gradient = QRadialGradient(-3, -3, 10)
        if option.state & QStyle.State_Sunken:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(1, QColor(Qt.yellow).lighter(120))
            gradient.setColorAt(0, QColor(Qt.darkYellow).lighter(120))
        else:
            gradient.setColorAt(0, Qt.yellow)
            gradient.setColorAt(1, Qt.darkYellow)

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(Qt.black, 0))
        painter.drawRect(rect)
        
        
        painter.setPen(Qt.white)
        painter.setBrush(Qt.lightGray)
        painter.drawText(self.x + 10, self.y + 20,"["+self.columns['Pid']+"]")
        painter.drawText(self.x + 10, self.y + 40,self.columns['Name'])


    def contextMenuEvent(self,contextMenuEvent):

        menu = QMenu()
        menu.triggered.connect(self.qmenuActionTriggered)

        menu.addAction("dlllist")
        menu.addAction("getsids")
        menu.addAction("privs")
        menu.addAction("handles")
        menu.exec_(contextMenuEvent.screenPos())


    def qmenuActionTriggered(self,action):
        
        self.ctxmenusignal.emit(self.columns,action.text())

   

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edgeList:
                edge.adjust()

        return super(Node, self).itemChange(change, value)

    
    def mouseDoubleClickEvent(self, event):
        self.update()
        super(Node, self).mouseDoubleClickEvent(event)


    
    def mousePressEvent(self, event):
        self.update()
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(Node, self).mouseReleaseEvent(event)


class GraphWidget(QGraphicsView):


    # this signal is sent when user right click --> click action in context menu
    CtxMenuActionClicked = pyqtSignal(dict,'QString',name='CtxMenuActionClicked')

    
    def __init__(self, model, parent=None):
        
        super(GraphWidget, self).__init__(parent)
        
        self.nodes = model.get_nodes() # retourne un dictionnaire
         
        # get root nodes
        
        roots = [] # identifiants des noeuds racines d'arbres
        for n in self.nodes.keys():
            root = True
            for nn in self.nodes.keys():

                if n in self.nodes[nn].get_node_children():
                    root = False
                    break
            if root :
                roots.append(n)
        
        
        self.i = 0
        self.noeuds = {} 
        
        r=0
        while ( r < len(roots)):
            self.printTree(roots[r],0)
            r+=1
        
        self.timerId = 0

        self.scene = QGraphicsScene(self)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.scene.setSceneRect(0, 0, self.i, 1000)
        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        for parent in self.noeuds.keys():
            self.scene.addItem(self.noeuds[parent])
            self.noeuds[parent].setPos(self.noeuds[parent].pos_x, self.noeuds[parent].pos_y)


        for parent in self.nodes.keys():

            for child in self.nodes[parent].get_node_children():
                
                self.scene.addItem(Edge(self.noeuds[parent], self.noeuds[child]))

       
        self.scale(0.2, 0.2)
        self.setMinimumSize(400, 400)
        self.setWindowTitle("PSTREE")

    def printTree(self,tree, depth):
        
        if (len(self.nodes[tree].get_node_children()) > 0):
            childs = self.nodes[tree].get_node_children()
            self.printTree(childs[0],depth + 100)

        
        columns = self.nodes[tree].get_node_columns()
        node = Node(self,self.i,depth,columns,self.CtxMenuActionClicked)
        self.i += 120
        self.noeuds[tree] = node
        
        j=1
        while(j<len(self.nodes[tree].get_node_children()) ):
            
            childs = self.nodes[tree].get_node_children()
            self.printTree(childs[j],depth + 100)
            j+=1

    
    
    def drawBackground(self, painter, rect):
        # Shadow.
        sceneRect = self.sceneRect()
        rightShadow = QRectF(sceneRect.right(), sceneRect.top() + 5, 5,
                sceneRect.height())
        bottomShadow = QRectF(sceneRect.left() + 5, sceneRect.bottom(),
                sceneRect.width(), 5)
        if rightShadow.intersects(rect) or rightShadow.contains(rect):
                painter.fillRect(rightShadow, Qt.darkGray)
        if bottomShadow.intersects(rect) or bottomShadow.contains(rect):
                painter.fillRect(bottomShadow, Qt.darkGray)

        # Fill.
        gradient = QLinearGradient(sceneRect.topLeft(), sceneRect.bottomRight())
        gradient.setColorAt(0, Qt.white)
        gradient.setColorAt(1, Qt.lightGray)
        painter.fillRect(rect.intersected(sceneRect), QBrush(gradient))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(sceneRect)

        # Text.
        textRect = QRectF(sceneRect.left() + 4, sceneRect.top() + 4, sceneRect.width() - 4, sceneRect.height() - 4)
        
        #message = "Click and drag the nodes around, and zoom with the " \
        #        "mouse wheel or the '+' and '-' keys"

        #font = painter.font()
        #font.setBold(True)
        #font.setPointSize(14)
        #painter.setFont(font)
        #painter.setPen(Qt.lightGray)
        #painter.drawText(textRect.translated(2, 2), message)
        #painter.setPen(Qt.black)
        #painter.drawText(textRect, message)

    def scaleView(self, scaleFactor):
        factor = self.transform().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)


    
    
    def itemMoved(self):
        
        pass
    
    def itemPressed(self,x,y):

        pass
       


    def qmenuActionTriggered(self,action):

        pass

        
    def keyPressEvent(self, event):

        key = event.key()

        if key == Qt.Key_Plus:
            self.scaleView(1.2)
        elif key == Qt.Key_Minus:
            self.scaleView(1 / 1.2)
        elif key == Qt.Key_Space or key == Qt.Key_Enter:
            for item in self.scene().items():
                if isinstance(item, Node):
                    item.setPos(-150 + qrand() % 300, -150 + qrand() % 300)
        else:
            super(GraphWidget, self).keyPressEvent(event)

    
    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.angleDelta().y() / 240.0))

    
    def mousePressEvent(self, event):
        
        if event.button() == Qt.MidButton: # or Qt.MiddleButton
            self.__prevMousePos = event.pos()
        else:
            super(GraphWidget, self).mousePressEvent(event)


    def mouseMoveEvent(self, event):
        
        if event.buttons() == Qt.MidButton: # or Qt.MiddleButton
            
            offset = self.__prevMousePos - event.pos()
            self.__prevMousePos = event.pos()

            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset.y())
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset.x())
        else:
            super(GraphWidget, self).mouseMoveEvent(event)

