import sys

from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(scene)
        self.setCentralWidget(self.view)

        self.view.viewport().setMouseTracking(True)
        self.view.scene().installEventFilter(self)

    def eventFilter(self, obj, event):
        if (
            obj is self.view.scene()
            and event.type() == QtCore.QEvent.GraphicsSceneMouseMove
        ):
            vp = self.view.mapFromScene(event.scenePos())
            if self.check_if_the_point_is_on_the_edge(vp, delta=10):
                print("on the border", event.scenePos())
        return super().eventFilter(obj, event)

    def check_if_the_point_is_on_the_edge(self, point, delta=1):
        rect = self.view.viewport().rect()
        internal_rect = rect.adjusted(delta, delta, -delta, -delta)
        return rect.contains(point) and not internal_rect.contains(point)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    w = MainWindow()
    w.show()
    w.resize(640, 480)

    sys.exit(app.exec_())