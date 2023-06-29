import sys
import time

from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt, QPoint, QRect, QPointF
from PyQt6.QtGui import QPainter, QPixmap, QPen, QColor, QImage, QBrush
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, \
    QGraphicsPixmapItem, QLabel, QColorDialog, QSizePolicy

from ui_v2.infrastructure.graphicObjects import DynamicProtectionElement, test_item


class Scene(QWidget):

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # cnv = Canvas(self.height(), self.width())
        # print(self.height(), self.width())
        cnv = ViewArea()
        lo = QVBoxLayout()
        lo.addWidget(cnv)
        self.setLayout(lo)


class ViewArea(QGraphicsView):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        self.scene = QGraphicsScene()
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setSceneRect(0, -self.scene.sceneRect().height()/2, self.scene.sceneRect().width(), self.scene.sceneRect().height())

        # draw some lines in scene
        # self.draw_axs()

        # self.scene.addText('LEBULEBUEB:ELBELBS')
        self.item1 = DynamicProtectionElement()
        # self.item2 = test_item()
        self.scene.addItem(self.item1)
        # self.scene.addItem(self.item2)

        # self.scale(2, 1)
        self.setScene(self.scene)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        print(event.mimeData().text())
        event.acceptProposedAction()

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF) -> None:
        background_brush = QtGui.QBrush(QtGui.QColor(255, 170, 255), Qt.BrushStyle.SolidPattern)
        pen = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.DashDotDotLine)
        painter.setPen(pen)
        painter.drawLine(QPointF(rect.bottomLeft().x(), rect.center().y()),
                         QPointF(rect.bottomRight().x(), rect.center().y()))


    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if event.angleDelta().y()>0:
            # self.scale(1.2, 1.2)
            # self.item1.setRotation(self.item1.rotation()+10)
            # print(self.item1.rotation())
            # self.item1.setScale(2)
            # self.item1.mack_thicker(1.2)
            # self.item1.mack_longer(1.1)
            self.item1.scale_object(1.1)
            self.scene.update()
            # self.repaint()
        else:
            # self.scale(0.8, 0.8)
            # self.item1.setRotation(self.item1.rotation()-10)
            # print(self.item1.rotation())
            # self.item1.setScale(0.5)
            # self.item1.mack_thicker(0.8)
            # self.item1.mack_longer(0.9)
            self.item1.scale_object(0.9)
            self.scene.update()
            # pass

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.MouseButton.RightButton:
    #         self._rightButtonPressed = True
    #         self._panStartX = event.pos().x()
    #         self._panStartY = event.pos().y()
    #         self.setCursor(Qt.CursorShape.ClosedHandCursor)

    # def mouseReleaseEvent(self, event):
    #     if event.button()==Qt.MouseButton.RightButton:
    #         self._rightButtonPressed = False
    #         self.setCursor(Qt.CursorShape.ArrowCursor)

    # def mouseMoveEvent(self, event):
    #     if self._rightButtonPressed:
    #         # self.scene.setSceneRect(self.sceneRect().translated(event.pos().x()-self._panStartX, event.pos().y()-self._panStartY))
    #         # self.setSceneRect(self.sceneRect().translated(event.pos().x()-self._panStartX, event.pos().y()-self._panStartY))
    #         self.scene.setSceneRect(self.scene.sceneRect().translated(event.pos().x()-self._panStartX, event.pos().y()-self._panStartY))
    #         # self.scene.setSceneRect(self.scene.sceneRect(). (event.pos().x()-self._panStartX, event.pos().y()-self._panStartY))
    #         # self.scene.sceneRect().moveTo(event.pos().x()-self._panStartX, event.pos().y()-self._panStartY)
    #         # self.viewport().move(self.viewport().x()+event.pos().x()-self._panStartX,
    #         #                      self.viewport().y()+event.pos().y()-self._panStartY)
    #         self._panStartX = event.pos().x()
    #         self._panStartY = event.pos().y()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        self.scene.update()
        super(ViewArea, self).mouseMoveEvent(event)

    # def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
    #     for i in self.scene.items():
    #         i.highlight_flag = False

    # def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
    #     self.scene.update()
    #     super(ViewArea, self).mousePressEvent(event)


# # Creates widget to be drawn on
# class Canvas(QLabel):
#
#     def __init__(self, width, height):
#         super().__init__()
#
#         # Create a pixmap object that will act as the canvas
#         self.pixmap = QPixmap(width, height)
#         self.pixmap.fill(Qt.GlobalColor.white)
#         self.setPixmap(self.pixmap)
#
#         # Keep track of the mouse for getting mouse coordinates
#         self.mouse_track_label = QLabel()
#         # self.setMouseTracking(True)
#
#         # Initialize variables
#         self.antialiasing_status = True
#         # self.eraser_selected = False
#
#         self.last_mouse_pos = QPoint()
#         self.drawing = False
#         self.pen_color = Qt.GlobalColor.red
#         self.pen_width = 2
#
#         self.composition_objects = []
#         self.composition_objects.append(DynamicProtectionElement())
#
#         self.drawComposition()
#
#
#     def drawComposition(self):
#         painter = QPainter(self.pixmap)
#         if self.antialiasing_status:
#             painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#
#         for i in self.composition_objects:
#             i.draw(painter, QPointF(250, 250))
#
#         self.update()
#
#     def mousePressEvent(self, event):
#         """Handle when mouse is pressed."""
#         if event.button() == Qt.MouseButton.LeftButton:
#             self.newCanvas()
#             self.composition_objects[-1].tilt_angle +=10
#             print(self.composition_objects[-1].tilt_angle)
#             self.drawComposition()
#
#
#     def mouseReleaseEvent(self, event):
#         """Handle when mouse is released.
#         Check when eraser is no longer being used."""
#         if event.button() == Qt.MouseButton.LeftButton:
#             self.drawing = False
#
#     def newCanvas(self):
#         """Clears the current canvas."""
#         self.pixmap.fill(Qt.GlobalColor.white) # fixme
#         self.update()
#
#     def paintEvent(self, event):
#         """Create QPainter object.
#         This is to prevent the chance of the painting being lost
#         if the user changes windows."""
#         painter = QPainter(self)
#         target_rect = QRect()
#         target_rect = event.rect()
#         painter.drawPixmap(target_rect, self.pixmap, target_rect)
#         painter.end()


if __name__=='__main__':
    app = QApplication(sys.argv)
    mw = QMainWindow()
    w = Scene()
    mw.setCentralWidget(w)
    mw.show()
    sys.exit(app.exec())