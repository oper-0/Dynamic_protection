import sys
import time
from typing import Callable

from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt, QPoint, QRect, QPointF
from PyQt6.QtGui import QPainter, QPixmap, QPen, QColor, QImage, QBrush
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, \
    QGraphicsPixmapItem, QLabel, QColorDialog, QSizePolicy

from ui_v2.infrastructure.graphicObjects import DynamicProtectionElement, test_item
from ui_v2.infrastructure.helpers import ItemsCollectionInterface


class GraphicsScene(QGraphicsScene):

    status_bar: Callable[[str], None]
    logger: Callable[[str,str], None]
    item_catalog: ItemsCollectionInterface


    # def __int__(self):
    #     self.setSceneRect(0, 0, self.GraphicsView.width(), self.GraphicsView.height())

    def drawForeground(self, painter, rect):
        super(GraphicsScene, self).drawForeground(painter, rect)
        if not hasattr(self, "cursor_position"):
            return
        painter.save()
        pen = QPen(Qt.GlobalColor.cyan)
        pen.setWidth(1)
        painter.setPen(pen)
        linex = QtCore.QLineF(
            rect.left(),
            self.cursor_position.y(),
            rect.right(),
            self.cursor_position.y(),
        )
        liney = QtCore.QLineF(
            self.cursor_position.x(),
            rect.top(),
            self.cursor_position.x(),
            rect.bottom(),
        )
        for line in (linex, liney):
            painter.drawLine(line)
        painter.restore()

    def mouseMoveEvent(self, event):
        self.cursor_position = event.scenePos()
        self.update()
        super(GraphicsScene, self).mouseMoveEvent(event)
        # print(self.cursor_position)
        self.status_bar(f"x:{int(self.cursor_position.x())} y:{int(self.cursor_position.y())}")

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        pass

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasText():
            event.setAccepted(True)
            self.dragOver = True
            self.update()


    # def dropEvent(self, event: QtGui.QDropEvent) -> None:
    def dropEvent(self, event: 'QGraphicsSceneDragDropEvent') -> None:
        name = event.mimeData().text()
        item_pos = event.scenePos()
        # item_pos = QPointF(event.position().x()-self.width()/2, event.position().y()-self.height()/2)
        # item_pos = self.release_pos
        self.logger(f"item dropped on {item_pos}", 'info')
        item = self.item_catalog.get_item(name)
        scene_item = item.get_scene_item()
        scene_item.set_position(item_pos)
        if not item:
            self.logger(f"Отсутствует соответствие названия в каталоге для {name}", 'error')
            event.acceptProposedAction()
            return

        self.addItem(scene_item)
        event.acceptProposedAction()



    # def __init__(self):
    #     super().__init__()
    #     self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    #     # cnv = Canvas(self.height(), self.width())
    #     # print(self.height(), self.width())
    #     cnv = ControlView()
    #     lo = QVBoxLayout()
    #     lo.addWidget(cnv)
    #     self.setLayout(lo)


class ControlView(QGraphicsView):
    cell_size = 80
    grid_pen = QPen(Qt.GlobalColor.lightGray, 1, Qt.PenStyle.DashDotDotLine)
    axis_pen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.DashDotDotLine)
    _zoom = 0
    # scene_items:list[] = []
    # ControlViewClicked = QtCore.pyqtSignal(QtCore.QPoint)

    # def __init__(self,
    #              item_catalog: ItemsCollectionInterface,
    #              logger_fun: Callable[[str, str], None],
    #              status_bar: Callable[[str], None],
    #              props_displayer: Callable[[dict, str], None]):
    def __init__(self,
                 item_catalog: ItemsCollectionInterface,
                 logger_fun: Callable[[str,str], None],
                 status_bar: Callable[[str], None]):
    # def __init__(self,
    #              item_catalog: ItemsCollectionInterface,
    #              logger_fun: Callable[[str,str], None]):
        super().__init__()

        # self.CVScene = QGraphicsScene()
        self.CVScene = GraphicsScene()
        self.CVScene.status_bar = status_bar
        self.CVScene.logger = logger_fun
        self.CVScene.item_catalog = item_catalog
        # self.CVScene.setSceneRect(self.rect().x(), self.rect().y(), self.width(), self.height())
        self.item_catalog = item_catalog
        self.logger = logger_fun

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setBackgroundBrush(Qt.GlobalColor.lightGray)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setObjectName('ControlView')
        self.setScene(self.CVScene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setAcceptDrops(True)
        # self.DragMode(QGraphicsView.DragMode.ScrollHandDrag)
        # self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.dragOver = False

    def mousePressEvent(self, event):
        # self.ControlViewClicked.emit(self.mapToScene(event.pos()).toPoint())
        # if event.button() == Qt.MouseButton.RightButton:
        #     self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        # else:
        #     self.setDragMode(QGraphicsView.DragMode.NoDrag)

        super(ControlView, self).mousePressEvent(event)

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF) -> None:
        painter.save()
        painter.setPen(self.grid_pen)
        # draw y lines
        y_pos = 0
        while y_pos>rect.top():
            painter.drawLine(QPointF(rect.left(), y_pos),
                             QPointF(rect.right(), y_pos),)
            y_pos-=self.cell_size
        y_pos = 0
        while y_pos<rect.bottom():
            painter.drawLine(QPointF(rect.left(), y_pos),
                             QPointF(rect.right(), y_pos),)
            y_pos+=self.cell_size

        # draw x lines
        x_pos = 0
        while x_pos>rect.left():
            painter.drawLine(QPointF(x_pos, rect.bottom()),
                             QPointF(x_pos, rect.top()),)
            x_pos-=self.cell_size
        x_pos = 0
        while x_pos<rect.right():
            painter.drawLine(QPointF(x_pos, rect.bottom()),
                             QPointF(x_pos, rect.top()),)
            x_pos+=self.cell_size

        # draw axis
        painter.setPen(self.axis_pen)
        painter.drawLine(QPointF(rect.left(), 0),QPointF(rect.right(), 0))
        painter.drawLine(QPointF(0, rect.bottom()),QPointF(0, rect.top()))


        painter.restore()

    # def wheelEvent(self, event):
    #     if event.angleDelta().y() > 0:
    #         factor = 1.25
    #         self._zoom += 1
    #     else:
    #         factor = 0.8
    #         self._zoom -= 1
    #     if self._zoom > 0:
    #         self.scale(factor, factor)
    #     elif self._zoom == 0:
    #         # self.fitInView()
    #         pass
    #     else:
    #         self._zoom = 0

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if event.angleDelta().y()>0:
            self.scale(1.1,1.1)
            # for i in self.items():
            #     i.scale_object(1.1)
            #     self.CVScene.update()
            # self.item1.scale_object(1.1)
        else:
            self.scale(0.9,0.9)
            # for i in self.items():
            #     i.scale_object(0.9)
            #     self.CVScene.update()



    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        self.CVScene.update()
        super(ControlView, self).mouseMoveEvent(event)


if __name__=='__main__':
    app = QApplication(sys.argv)
    mw = QMainWindow()
    w = Scene()
    mw.setCentralWidget(w)
    mw.show()
    sys.exit(app.exec())