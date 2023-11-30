import functools
from abc import ABC, abstractmethod
from typing import Protocol, Callable  # i really want to use this but abc should be best practice here

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QMimeData, QEvent
from PyQt6.QtGui import QPixmap, QFont, QDragEnterEvent, QDropEvent, QMouseEvent, QDrag
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QApplication, QGraphicsOpacityEffect


class SceneItemAbstract:
    title: str
    img: QPixmap


class UnknownItem(SceneItemAbstract):

    def __init__(self):
        self.title = 'Unknown'


class SceneItemWidget(QWidget):

    def __init__(self,
                 title: str = 'unknown',
                 description: str = 'unknown',
                 img_path: str = '',
                 actor: Callable[[], None] = lambda *args: None,
                 column_count=2,
                 block=False): # todo finish me
        super().__init__()
        layout = QVBoxLayout()


        self.title = title
        self.description = description
        self.actor = actor
        self.block = block

        #   image to item:
        self.lb = QLabel()
        if column_count==1:
            pm = QPixmap(img_path).scaled(200, 100, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        elif column_count==2:
            pm = QPixmap(img_path).scaled(100, 100, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        else:
            pm = QPixmap(img_path)
        self.lb.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.lb.setPixmap(pm)
        layout.addWidget(self.lb)


        #   title to item
        self.title_text_label = QLabel(self.title)
        self.title_text_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.title_text_label.setFont(QFont('Courier New'))
        if self.block:
            self.title_text_label.setStyleSheet('color: gray')
        else:
            self.title_text_label.setStyleSheet('color: black')
        layout.addWidget(self.title_text_label)

        #   tooltip for item
        if self.block:
            self.setToolTip("[В разработке] "+self.description)
        else:
            self.setToolTip(self.description)

        self.setLayout(layout)

        if self.block:
            self.setGraphicsEffect(QGraphicsOpacityEffect())


    def get_scene_item(self):
        return self.actor()

    def block_decorator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.block:
                # print("blocked")
                result = None
            else:
                result = method(self, *args, **kwargs)
            return result
        return wrapper

    @block_decorator
    def mousePressEvent(self, e):

        if e.button() != Qt.MouseButton.LeftButton:
            return
        self.lb.setStyleSheet('background: lightGray')
        self.title_text_label.setStyleSheet('color: black')
        # self.setGraphicsEffect(QtWidgets.QGraphicsColorizeEffect())
        self.drag_start_position = e.pos()

    @block_decorator
    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if not (e.buttons() & Qt.MouseButton.LeftButton):
            return
        if (e.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        self.lb.setStyleSheet('background: transparent')
        self.title_text_label.setStyleSheet('color: gray')

        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.title)
        drag.setMimeData(mimedata)
        # drag.setPixmap(self.lb.pixmap().scaled(24, 24))
        drag.setPixmap(self.lb.pixmap())
        # print(self.lb.size())
        drag.setHotSpot(e.pos())
        # drag.setHotSpot(e.position())
        drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)


    @block_decorator
    def mouseReleaseEvent(self, e):
        self.lb.setStyleSheet('background: transparent')
        self.title_text_label.setStyleSheet('color: gray')
        # self.setGraphicsEffect(QtWidgets.Ef)


class SceneItemWidgetSHELL(QWidget):

    def __init__(self, title: str = 'unknown', description: str = 'unknown', img_path: str = '', actor: Callable[[], None] = lambda *args: None, column_count=2): # todo finish me
        super().__init__()
        layout = QVBoxLayout()


        self.title = title
        self.description = description
        self.actor = actor

        #   image to item:
        self.lb = QLabel()
        if column_count==1:
            pm = QPixmap(img_path).scaled(200, 100, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        elif column_count==2:
            pm = QPixmap(img_path).scaled(100, 100, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        else:
            pm = QPixmap(img_path)
        self.lb.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.lb.setPixmap(pm)
        layout.addWidget(self.lb)


        #   title to item
        self.title_text_label = QLabel(self.title)
        self.title_text_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.title_text_label.setFont(QFont('Courier New'))
        self.title_text_label.setStyleSheet('color: gray')
        layout.addWidget(self.title_text_label)

        #   tooltip for item
        self.setToolTip(description)

        self.setLayout(layout)

    def get_scene_item(self):
        return self.actor()

    def mousePressEvent(self, e):
        if e.button() != Qt.MouseButton.LeftButton:
            return
        self.lb.setStyleSheet('background: lightskyblue')
        self.title_text_label.setStyleSheet('color: black')
        # self.setGraphicsEffect(QtWidgets.QGraphicsColorizeEffect())
        # self.drag_start_position = e.pos()


    # def mouseReleaseEvent(self, e):
    #     self.lb.setStyleSheet('background: transparent')
    #     self.title_text_label.setStyleSheet('color: gray')
        # self.setGraphicsEffect(QtWidgets.Ef)