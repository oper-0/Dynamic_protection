import random
import string
import sys
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QPalette
from PyQt6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QMainWindow, QApplication


class CalculatorWidget(QWidget):

    def __init__(self):
        super().__init__()

    def show_single_items_calcs(self):
        ...



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QMainWindow()
    w.show()
    w.setCentralWidget(CalculatorWidget())
    app.exec()
