import math
import random
from PyQt6 import QtCore, QtGui, QtWidgets


class Circle(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, *args, **kwargs):
        self._line = QtCore.QLineF()
        super().__init__(*args, **kwargs)
        # Flags to allow dragging and tracking of dragging.
        self.setFlags(
            self.flags()
            | QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, line):
        self._line = line

    def itemChange(self, change, value):
        if (
            change == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemPositionChange
            and self.isSelected()
            and not self.line.isNull()
        ):
            # http://www.sunshine2k.de/coding/java/PointOnLine/PointOnLine.html
            p1 = self.line.p1()
            p2 = self.line.p2()
            e1 = p2 - p1
            e2 = value - p1
            dp = QtCore.QPointF.dotProduct(e1, e2)
            l = QtCore.QPointF.dotProduct(e1, e1)
            p = p1 + dp * e1 / l
            return p
        return super().itemChange(change, value)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    scene = QtWidgets.QGraphicsScene(QtCore.QRectF(-200, -200, 400, 400))
    view = QtWidgets.QGraphicsView(scene)

    points = (
        QtCore.QPointF(*random.sample(range(-150, 150), 2)) for _ in range(4)
    )
    angles = (math.pi / 4, math.pi / 3, math.pi / 5, math.pi / 2)

    for point, angle in zip(points, angles):
        item = Circle(QtCore.QRectF(-10, -10, 20, 20))
        item.setBrush(QtGui.QColor("salmon"))
        scene.addItem(item)
        item.setPos(point)
        end = 100 * QtCore.QPointF(math.cos(angle), math.sin(angle))
        line = QtCore.QLineF(QtCore.QPointF(), end)
        item.line = line.translated(item.pos())
        line_item = scene.addLine(item.line)
        line_item.setPen(QtGui.QPen(QtGui.QColor("green"), 4))

    view.resize(640, 480)
    view.show()

    sys.exit(app.exec())