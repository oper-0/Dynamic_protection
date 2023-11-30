
import random
import string
import sys
from typing import Callable, Protocol

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QPalette, QMovie
from PyQt6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QMainWindow, QApplication, QVBoxLayout, QLabel, \
    QHBoxLayout, QFormLayout


class DisplayerProtocol(Protocol):
    def set_data(self, data: dict) -> None:
        pass

    def set_widget(self, widget: QWidget) -> None:
        pass


class ResultDisplayer(QListWidget):

    def __init__(self):
        super().__init__()

        self.empty_data_mocker_layout = None
        self.gif_label = None
        self.empty_data_mocker_wgt = None
        self.data_layout = None # QFormLayout

        self.base_layout = QVBoxLayout()

        # self.setFont(QFont('Courier New', 12))

        self.setLayout(self.base_layout)

        self.spawn_empty()

        self.set_data({'aaaaa': 123, 'bbbbbb':3432, 'asdfas': 12342134})

        # self.my_style = """
        #                 QLabel {
        #                     font-size: 20px;
        #                     color: #333;
        #                 }
        #             """
        self.stl = """
            QFormLayout {
                border: 1px solid #ccc;  /* Рамка вокруг таблицы */
            }

            QLabel, QLineEdit {
                padding: 8px;  /* Внутренний отступ для элементов */
                border-bottom: 1px solid #ccc;  /* Разделяющая линия между строками */
            }

            QLabel {
                font-weight: bold;  /* Жирный шрифт для заголовков */
                background-color: #f0f0f0;  /* Цвет фона для заголовков */
            }

            QLineEdit {
                border: none;  /* Убираем рамку для QLineEdit */
            }
        """

        self.setStyleSheet(self.stl)

        self.show()

    def spawn_empty(self):
        # layout
        self.empty_data_mocker_layout = QHBoxLayout()

        # label
        self.empty_data_mocker_wgt = QLabel("Окно демонстрации результатов расчёта 🔠")
        self.empty_data_mocker_wgt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_data_mocker_wgt.setFont(QFont('Courier New', 12))
        self.empty_data_mocker_wgt.setStyleSheet('color: gray')
        self.empty_data_mocker_layout.addWidget(self.empty_data_mocker_wgt)

        # animation
        # self.gif_label = QLabel()
        # self.gif_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        # self.empty_data_mocker_layout.addWidget(self.gif_label)
        # movie = QMovie(r"C:\Users\4NR_Operator_34\Pictures\dog-doggo.gif") # TODO DELETE ME PLS
        # movie.setScaledSize(QSize(100, 100))
        # self.gif_label.setMovie(movie)
        # movie.start()

        self.base_layout.addLayout(self.empty_data_mocker_layout)

    def set_data(self, data: dict):
        self.clear()
        self.data_layout = QFormLayout()
        for key in data:
            self.data_layout.addRow(key, QLabel(str(data.get(key))))
        self.base_layout.addLayout(self.data_layout)


    def set_widget(self, widget: QWidget):
        ...

    def clear(self):
        clear_layout(self.base_layout)


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            clear_layout(item.layout())

if __name__=='__main__':
    app = QApplication(sys.argv)
    w = QMainWindow()
    w.show()
    w.setCentralWidget(ResultDisplayer())
    app.exec()