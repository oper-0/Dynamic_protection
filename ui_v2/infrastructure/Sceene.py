import sys
import time
from typing import Callable

from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt, QPoint, QRect, QPointF, QLine, QLineF, QRectF
from PyQt6.QtGui import QPainter, QPixmap, QPen, QColor, QImage, QBrush, QTextOption
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, \
    QGraphicsPixmapItem, QLabel, QColorDialog, QSizePolicy, QGraphicsTextItem, QScrollBar

from ui_v2.infrastructure.graphicObjects import DynamicProtectionElement, test_item
from ui_v2.infrastructure.helpers import ItemsCollectionInterface, TextOnScene
from ui_v2.infrastructure.semi_inf_isotropic_element import NEW_SemiInfIsotropicElement


class GraphicsScene(QGraphicsScene):

    status_bar: Callable[[str], None]
    logger: Callable[[str,str], None]
    item_catalog: ItemsCollectionInterface

    scene_obj_distance_lines: list[QLineF]
    scene_obj_distance_vertical_lines: list[QLineF]
    scene_obj_distance_text: list[TextOnScene]
    # scene_obj_distance_text_options: QTextOption = QTextOption(Qt.AlignmentFlag.AlignCenter)

    distance_lines_pen = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine)
    distance_vertical_lines_pen = QPen(Qt.GlobalColor.darkRed, 1, Qt.PenStyle.DashLine)

    rect_area: QRectF = QRectF(0, 0, 0, 0)  # FIXME лучше б получать эту арею из вью а не сцены

    v_line_delta = 150



    # def __int__(self):
    #     self.setSceneRect(0, 0, self.GraphicsView.width(), self.GraphicsView.height())
    def get_rect_area(self)->QRectF:
        return QRectF(
            self.rect_area.topLeft().x(),
            self.rect_area.topLeft().y()*1.5,
            self.rect_area.width()*1.5,
            self.rect_area.height()*1.5,
        )

    def drawForeground(self, painter, rect):
        super(GraphicsScene, self).drawForeground(painter, rect)
        painter.save()

        # save rect for closure call when drawing semi infinte isoropic item
        self.rect_area = rect

        # DRAW DISTANCE-LINES BETWEEN OBJECTS ON THE SCENE
        self.scene_obj_distance_lines = []
        self.scene_obj_distance_vertical_lines = []
        self.scene_obj_distance_text = []
        obj_positions: list[QPointF] = self._get_obj_positions(y_delta=self.v_line_delta)
        obj_positions.sort(key=lambda p: p.x())
        if len(obj_positions)>1:
            prev_pos = obj_positions[0]

            # first vertical line
            # v_line = QLineF(prev_pos, QPointF(prev_pos.x(), prev_pos.y() + self.v_line_delta))
            v_line = QLineF(QPointF(prev_pos.x(), 0), prev_pos)
            self.scene_obj_distance_vertical_lines.append(v_line)

            for obj_pos in obj_positions[1:]:
                # horizontal line
                line = QLineF(prev_pos, obj_pos)
                self.scene_obj_distance_lines.append(line)

                # vertical line
                # v_line = QLineF(obj_pos, QPointF(obj_pos.x(), obj_pos.y()+self.v_line_delta))
                v_line = QLineF(QPointF(obj_pos.x(), 0), obj_pos)
                self.scene_obj_distance_vertical_lines.append(v_line)

                text_item = TextOnScene(
                    position=QPointF(line.p1().x()+line.length()/2, line.p1().y()+15),
                    text=f'{int(line.length())}'
                )
                self.scene_obj_distance_text.append(text_item)

                prev_pos = obj_pos
            # v lines
            painter.setPen(self.distance_vertical_lines_pen)
            painter.drawLines(self.scene_obj_distance_vertical_lines)
            # h lines
            painter.setPen(self.distance_lines_pen)
            painter.drawLines(self.scene_obj_distance_lines)
            # text
            for ti in self.scene_obj_distance_text:
                painter.drawText(ti.position, ti.text)

        #  DRAW CROSS UNDER MOUSE
        if not hasattr(self, "cursor_position"):
            return
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

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self._unfocus_items()
        super(GraphicsScene, self).mousePressEvent(event)

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        pass

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasText():
            event.setAccepted(True)
            self.dragOver = True
            self.update()


    # def dropEvent(self, event: QtGui.QDropEvent) -> None:
    def dropEvent(self, event: 'QGraphicsSceneDragDropEvent') -> None:
        self._unfocus_items()
        name = event.mimeData().text()
        item = self.item_catalog.get_item(name)
        scene_item = item.get_scene_item()

        # 💩 magic code, do not touch:
        if hasattr(scene_item, 'get_half_height') and callable(scene_item.get_half_height):
            # item_pos = QPointF(event.scenePos().x(), 0-scene_item.get_half_height())
            item_pos = QPointF(event.scenePos().x(), 0)
            self.logger(f"item dropped on {item_pos}", 'info')

        if not item:
            self.logger(f"Отсутствует соответствие названия в каталоге для {name}", 'error')
            event.acceptProposedAction()
            return

        # 💩 magic code, do not touch:
        if hasattr(scene_item, 'set_props') and callable(scene_item.set_props):
            scene_item.set_props()
        else:
            scene_item.set_position(item_pos)
            self.addItem(scene_item)

        event.acceptProposedAction()

    def _get_obj_positions(self, y_delta = 0):
        itms = self.items(Qt.SortOrder.AscendingOrder)
        poss = []
        for i in itms:
            # poss.append(QPointF(i.get_center().x(), i.get_center().y()+y_delta))
            poss.append(QPointF(i.scenePos().x(), i.scenePos().y()+y_delta))
        return poss

    def _unfocus_items(self):
        for itm in self.items():
            itm.unfocus()

class ControlView(QGraphicsView):
    cell_size = 80
    grid_pen = QPen(Qt.GlobalColor.lightGray, 1, Qt.PenStyle.DashDotDotLine)
    axis_pen = QPen(Qt.GlobalColor.white, 1, Qt.PenStyle.SolidLine)
    axis_pen_x = QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.DashLine)
    _zoom = 0

    _isPanning = False
    _mousePressed = False
    def __init__(self,
                 item_catalog: ItemsCollectionInterface,
                 logger_fun: Callable[[str,str], None],
                 status_bar: Callable[[str], None]):
        super().__init__()

        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)

        self.CVScene = GraphicsScene()
        self.CVScene.status_bar = status_bar
        self.CVScene.logger = logger_fun
        self.CVScene.item_catalog = item_catalog

        # Элемент полу-бесконечной брони
        self.semi_inf_isotropic_element = NEW_SemiInfIsotropicElement(
            property_displayer = lambda x: print(f'displaying property: {x}'),
            f_get_scene_rect = self.CVScene.get_rect_area)
        self.CVScene.addItem(self.semi_inf_isotropic_element())

        self.item_catalog = item_catalog
        self.logger = logger_fun

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)


        # self.hScrollBar = QScrollBar()
        # self.hScrollBar.setGeometry(100, 50,30,200)
        # self.hScrollBar.setValue(25)
        # self.setHorizontalScrollBar(self.hScrollBar)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


        self.setBackgroundBrush(Qt.GlobalColor.lightGray)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setObjectName('ControlView')
        self.setScene(self.CVScene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setAcceptDrops(True)
        self.dragOver = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._mousePressed = True
            if self._isPanning:
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
                self._dragPos = event.pos()
                event.accept()
            else:
                super(ControlView, self).mousePressEvent(event)

        # super(ControlView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self._mousePressed = False
        super(ControlView, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Space and not self._mousePressed:
            self._isPanning = True
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        else:
            super(ControlView, self).keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Space:
            if not self._mousePressed:
                self._isPanning = False
                self.setCursor(Qt.CursorShape.ArrowCursor)
            else:
                super(ControlView, self).keyReleaseEvent(event)

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
        painter.setPen(self.axis_pen_x)
        painter.drawLine(QPointF(rect.left(), 0),QPointF(rect.right(), 0))
        painter.setPen(self.axis_pen)
        painter.drawLine(QPointF(0, rect.bottom()),QPointF(0, rect.top()))


        painter.restore()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if event.angleDelta().y()>0:
            self.scale(1.1,1.1)
        else:
            self.scale(0.9,0.9)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        self.CVScene.update()
        if self._mousePressed and self._isPanning:
            newPos = event.pos()
            # newPos = event.position()
            diff = newPos - self._dragPos
            self._dragPos = newPos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()-diff.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value()-diff.y())
            print(self.verticalScrollBar().value())
            event.accept()
        else:
            super(ControlView, self).mouseMoveEvent(event)
