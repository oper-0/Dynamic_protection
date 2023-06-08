import sys
import time

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QPoint, QRect, QPointF
from PyQt6.QtGui import QPainter, QPixmap, QPen, QColor, QImage, QBrush
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, \
    QGraphicsPixmapItem, QLabel, QColorDialog, QSizePolicy

from ui_v2.infrastructure.graphicObjects import DynamicProtectionElement


class Scene(QWidget):

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        cnv = Canvas(self.height(), self.width())
        lo = QVBoxLayout()
        lo.addWidget(cnv)
        self.setLayout(lo)



# Creates widget to be drawn on
class Canvas(QLabel):

    def __init__(self, width, height):
        super().__init__()

        # Create a pixmap object that will act as the canvas
        self.pixmap = QPixmap(width, height)
        self.pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(self.pixmap)

        # Keep track of the mouse for getting mouse coordinates
        self.mouse_track_label = QLabel()
        # self.setMouseTracking(True)

        # Initialize variables
        self.antialiasing_status = True
        # self.eraser_selected = False

        self.last_mouse_pos = QPoint()
        self.drawing = False
        self.pen_color = Qt.GlobalColor.red
        self.pen_width = 2

        self.composition_objects = []
        self.composition_objects.append(DynamicProtectionElement())

        self.drawComposition()


    def drawComposition(self):
        painter = QPainter(self.pixmap)
        if self.antialiasing_status:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for i in self.composition_objects:
            i.draw(painter, QPointF(250, 250))

        self.update()

    def mousePressEvent(self, event):
        """Handle when mouse is pressed."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.newCanvas()
            self.composition_objects[-1].tilt_angle +=10
            print(self.composition_objects[-1].tilt_angle)
            self.drawComposition()


    def mouseReleaseEvent(self, event):
        """Handle when mouse is released.
        Check when eraser is no longer being used."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def newCanvas(self):
        """Clears the current canvas."""
        self.pixmap.fill(Qt.GlobalColor.white) # fixme
        self.update()

    def paintEvent(self, event):
        """Create QPainter object.
        This is to prevent the chance of the painting being lost
        if the user changes windows."""
        painter = QPainter(self)
        target_rect = QRect()
        target_rect = event.rect()
        painter.drawPixmap(target_rect, self.pixmap, target_rect)
        painter.end()


if __name__=='__main__':
    app = QApplication(sys.argv)
    mw = QMainWindow()
    w = Scene()
    mw.setCentralWidget(w)
    mw.show()
    sys.exit(app.exec())