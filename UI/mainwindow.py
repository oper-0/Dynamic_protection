# -*- coding: utf-8 -*-

import sys

from PyQt6 import QtGui
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6.QtWidgets import QFormLayout, QLineEdit, QWidget


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.calculate_btn = QPushButton("Рассчитать")
        self.calculate_btn.pressed.connect(self.calc_start)

        self.statusBar().showMessage("StatusBar")

        #  Параметры окна
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle("Расчет ДЗ")
        self.setWindowIcon(QtGui.QIcon(r"icons\star.png"))

        # Поля ввода данных
        self.coeff_nu_edit = QLineEdit()
        self.pl_front_thickness_edit = QLineEdit()
        self.pl_back_thickness_edit = QLineEdit()
        self.angle = QLineEdit()
        self.pl_front_density = QLineEdit()
        self.pl_back_density = QLineEdit()
        self.pl_lim_fluidity = QLineEdit()
        self.pl_length = QLineEdit()
        self.pl_width = QLineEdit()
        self.explosive_layer_height = QLineEdit()
        self.explosive_density = QLineEdit()
        self.detonation_velocity = QLineEdit()
        self.crit_dim_detonation = QLineEdit()
        self.stream_density = QLineEdit()
        self.stream_lim_fluidity = QLineEdit()
        self.stream_dim = QLineEdit()
        self.stream_velocity = QLineEdit()
        self.polytropy_index = QLineEdit()
        self.ksi_z = QLineEdit()
        self.ksi_r = QLineEdit()
        self.detonation_pressure = QLineEdit()
        self.coeff_avr_pressure = QLineEdit()
        self.coeff_stream_dim_extension = QLineEdit()

        # Добавляем поля ввода в Layout
        formLayout = QFormLayout()
        formLayout.addRow(self.tr("&Эмпирический коэффициент:"),
                          self.coeff_nu_edit)
        formLayout.addRow(self.tr("&Толщина пластины (лицевой):"),
                          self.pl_front_thickness_edit)
        formLayout.addRow(self.tr("&Толщина пластины (тыльной):"),
                          self.pl_back_thickness_edit)
        # formLayout.addRow((self.tr("&Карта")))
        formLayout.addRow(self.calculate_btn)

        # self.setCentralWidget(formLayout)

        widget = QWidget()
        widget.setLayout(formLayout)
        self.setCentralWidget(widget)

        self.show()

    def calc_start(self):
        print("calc")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
