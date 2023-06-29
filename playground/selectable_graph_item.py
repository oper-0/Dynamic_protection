import sys
from PyQt4 import QtGui, QtCore

class GraphicsItem(QtGui.QGraphicsItem):
    #
    # QtGui.QGraphicsItem always needs to override its two public abstract methods
    # paint, boundingRect
    #
    def __init__(self, rect=None, parent=None):
        super(GraphicsItem, self).__init__(parent)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        self.pen = QtGui.QPen(QtCore.Qt.SolidLine)
        self.pen.setColor(QtCore.Qt.blue)
        self.pen.setWidth(8)
        self.brush = QtGui.QBrush(QtCore.Qt.red)

        self.rect = QtCore.QRectF(rect[0], rect[1], rect[2], rect[3])

    def mouseMoveEvent(self, event):
        # move object
        QtGui.QGraphicsItem.mouseMoveEvent(self, event)

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawEllipse(self.rect)


class MyMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

        width = 1000
        height = 800
        scene = QtGui.QGraphicsScene(-width/2, -height/2, width, height)

        graphicsItem = GraphicsItem((-100, -100, 200, 200))
        scene.addItem(graphicsItem)

        view = QtGui.QGraphicsView()
         # set QGraphicsView attributes
        view.setRenderHints(QtGui.QPainter.Antialiasing |
                            QtGui.QPainter.HighQualityAntialiasing)
        view.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)

        view.setScene(scene)
        self.setCentralWidget(view)

    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_Escape:
            sys.exit(QtGui.qApp.quit())
        else:
            super(GraphicsView, self).keyPressEvent(event)

def main():
    app = QtGui.QApplication(sys.argv)
    form = MyMainWindow()
    form.setGeometry(700, 100, 1050, 850)
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()