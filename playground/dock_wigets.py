import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QDockWidget, QWidget, QMainWindow


class Dock_1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def sizeHint(self):
        # return QSize(.2 * self.width(), .7 * self.height())
        return QSize(2 * self.width(), 7 * self.height())


class Dock_2(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def sizeHint(self):
        # return QSize(.2 * self.width(), .3 * self.height())
        return QSize(2 * self.width(), 3 * self.height())


class Dock_3(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def sizeHint(self):
        # return QSize(.6 * self.width(), .7 * self.height())
        return QSize(6 * self.width(), 7 * self.height())


class Dock_4(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def sizeHint(self):
        # return QSize(.6 * self.width(), .3 * self.height())
        return QSize(6 * self.width(), 3 * self.height())


class Dock_5(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def sizeHint(self):
        # return QSize(.1 * self.width(), self.height())
        return QSize(1 * self.width(), self.height())


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 800, 800)
        self.UiComponents()
        self.show()

    def UiComponents(self):
        dock1 = QDockWidget("Dock_1", self)
        dock2 = QDockWidget("Dock_2", self)
        dock3 = QDockWidget("Dock_3", self)
        dock4 = QDockWidget("Dock_4", self)
        dock5 = QDockWidget("Dock_5", self)

        dock1.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        dock2.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        dock3.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        dock4.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        dock5.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        w_1 = Dock_1()
        w_2 = Dock_2()
        w_3 = Dock_3()
        w_4 = Dock_4()
        w_5 = Dock_5()

        dock1.setWidget(w_1)
        dock2.setWidget(w_2)
        dock3.setWidget(w_3)
        dock4.setWidget(w_4)
        dock5.setWidget(w_5)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock1)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock2)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock3)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock4)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock5)

        self.splitDockWidget(dock1, dock2, Qt.Orientation.Vertical)
        self.splitDockWidget(dock3, dock5, Qt.Orientation.Horizontal)
        self.splitDockWidget(dock3, dock4, Qt.Orientation.Vertical)

        self.docks = dock1, dock2, dock3, dock4, dock5

    def resizeEvent(self, event):
        super().resizeEvent(event)
        side = self.width() // 5 # 2 / 10
        center = side * 3 # 6 / 10
        widths = side, side, center, center, side
        self.resizeDocks(self.docks, widths, Qt.Orientation.Horizontal)
        vUnit = self.height() // 10
        top = vUnit * 7
        bottom = vUnit * 3
        heights = top, bottom, top, bottom, top + bottom
        self.resizeDocks(self.docks, heights, Qt.Orientation.Vertical)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    # w.show()
    sys.exit(app.exec())