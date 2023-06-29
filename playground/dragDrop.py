import sys

from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor
from PyQt5.QtCore import QMimeData, Qt


class DraggableLabel(QLabel):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.text())
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)

class DropLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.pos()
        text = event.mimeData().text()
        self.setText(text)
        event.acceptProposedAction()

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label = DropLabel("drop there",self)
        label.setGeometry(190, 65, 100,100)

        label_to_drag = DraggableLabel("drag this",self)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())


# #!/usr/bin/python
#
# """
# ZetCode PyQt6 tutorial
#
# This is a simple drag and
# drop example.
#
# Author: Jan Bodnar
# Website: zetcode.com
# """
#
# import sys
#
# from PyQt6.QtWidgets import (QPushButton, QWidget,
#         QLineEdit, QApplication)
#
#
# class Button(QPushButton):
#
#     def __init__(self, title, parent):
#         super().__init__(title, parent)
#
#         self.setAcceptDrops(True)
#
#
#     def dragEnterEvent(self, e):
#
#         if e.mimeData().hasFormat('text/plain'):
#             e.accept()
#         else:
#             e.ignore()
#
#
#     def dropEvent(self, e):
#
#         self.setText(e.mimeData().text())
#
#
# class Example(QWidget):
#
#     def __init__(self):
#         super().__init__()
#
#         self.initUI()
#
#
#     def initUI(self):
#
#         edit = QLineEdit('', self)
#         edit.setDragEnabled(True)
#         edit.move(30, 65)
#
#         button = Button("Button", self)
#         button.move(190, 65)
#
#         self.setWindowTitle('Simple drag and drop')
#         self.setGeometry(300, 300, 300, 150)
#
#
# def main():
#
#     app = QApplication(sys.argv)
#     ex = Example()
#     ex.show()
#     app.exec()
#
#
# if __name__ == '__main__':
#     main()