
"""widgets for graphicsObjects"""
import sys
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSlider, QLabel, QApplication, QMainWindow, QDoubleSpinBox


class LabelAndSlider(QWidget):
    # def __init__(self, f_on_change = Callable[[int], None]):
    def __init__(self, min_val, max_val, val, postfix=''):
        super().__init__()
        self.layout = QHBoxLayout()

        # self.f_on_change = f_on_change

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(min_val)
        self.slider.setMaximum(max_val)
        self.slider.setValue(val)
        self.slider.valueChanged.connect(self._update_label)

        self.label = QLabel(f'{val}{postfix}')

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)

        self.setLayout(self.layout)

    def _update_label(self, value):
        # self.label.setText(str(value))
        self.label.setText(f'{value}°')
        # self.f_on_change(value)


class LabelAndSpin(QWidget):
    # def __init__(self, f_on_change = Callable[[int], None]):
    def __init__(self, val, postfix=''):
        super().__init__()
        self.layout = QHBoxLayout()

        # self.f_on_change = f_on_change

        self.spin = QDoubleSpinBox()
        self.spin.setValue(val)
        self.spin.valueChanged.connect(self._update_label)

        self.label = QLabel(f'{val}{postfix}')

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spin)

        self.setLayout(self.layout)

    def _update_label(self, value):
        # self.label.setText(str(value))
        self.label.setText(f'{value}°')
        # self.f_on_change(value)


class DoubleSpinBoxMod1(QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.setMaximum(1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = QMainWindow()
    ex = LabelAndSlider()
    mw.setCentralWidget(ex)
    mw.show()
    sys.exit(app.exec())