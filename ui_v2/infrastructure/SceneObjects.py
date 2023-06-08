from abc import ABC, abstractmethod
from typing import Protocol  # i really want to use this but abc should be best practice here

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy


class SceneItemAbstract:
    title: str
    img: QPixmap


class UnknownItem(SceneItemAbstract):

    def __init__(self):
        self.title = 'Unknown'


class SceneItemWidget(QWidget):

    def __init__(self, title: str, description: str, img_path: str): # todo finish me
        super().__init__()
        layout = QVBoxLayout()

        self.title = title
        self.description = description

        #   image to item:
        self.lb = QLabel()
        pm = QPixmap(img_path).scaled(100, 100)
        # pm = QPixmap(img_path).scaled(200, 200)
        self.lb.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.lb.setPixmap(pm)
        layout.addWidget(self.lb)


        #   title to item
        self.title_text = QLabel(self.title)
        self.title_text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.title_text.setFont(QFont('Courier New'))
        self.title_text.setStyleSheet('color: gray')
        layout.addWidget(self.title_text)

        #   tooltip for item
        self.setToolTip(description)

        self.setLayout(layout)

    def mousePressEvent(self, e):
        self.lb.setStyleSheet('background: lightGray')
        self.title_text.setStyleSheet('color: black')
        # self.pm.
        # self.setGraphicsEffect(QtWidgets.QGraphicsColorizeEffect())


    def mouseReleaseEvent(self, e):
        self.lb.setStyleSheet('background: transparent')
        self.title_text.setStyleSheet('color: gray')
        # self.setGraphicsEffect(QtWidgets.Ef)