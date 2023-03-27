# -*- coding: utf-8 -*-

import sys

from PyQt6 import QtCore
# from PyQt6 import QtGui as
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QToolBar
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
        self.setWindowIcon(QIcon(r"icons\star.png"))

        # Поля ввода данных.
        # Поля для параметров пластины
        self.coeff_nu_edit = QLineEdit()
        self.pl_front_thickness_edit = QLineEdit()
        self.pl_back_thickness_edit = QLineEdit()
        self.angle_edit = QLineEdit()
        self.pl_front_density_edit = QLineEdit()
        self.pl_back_density_edit = QLineEdit()
        self.pl_lim_fluidity_edit = QLineEdit()
        self.pl_length_edit = QLineEdit()
        self.pl_width_edit = QLineEdit()
        # Поля для параметров ВВ
        self.explosive_layer_height_edit = QLineEdit()
        self.explosive_density_edit = QLineEdit()
        self.detonation_velocity_edit = QLineEdit()
        self.crit_dim_detonation_edit = QLineEdit()
        # Поля для параметров струи
        self.stream_density_edit = QLineEdit()
        self.stream_lim_fluidity_edit = QLineEdit()
        self.stream_dim_edit = QLineEdit()
        self.stream_velocity_edit = QLineEdit()
        # Поля для остальных параметров
        self.polytropy_index_edit = QLineEdit()
        self.ksi_z_edit = QLineEdit()
        self.ksi_r_edit = QLineEdit()
        self.detonation_pressure_edit = QLineEdit()
        self.coeff_avr_pressure_edit = QLineEdit()
        self.coeff_stream_dim_extension_edit = QLineEdit()

        # Добавляем поля ввода в Layout.
        # Добавляем поля пластины
        formLayout = QFormLayout()
        formLayout.addRow(self.tr("&Эмпирический коэффициент:"),
                          self.coeff_nu_edit)
        formLayout.addRow(self.tr("&Толщина пластины (лицевой):"),
                          self.pl_front_thickness_edit)
        formLayout.addRow(self.tr("&Толщина пластины (тыльной):"),
                          self.pl_back_thickness_edit)
        formLayout.addRow(self.tr("&Угол между КС и нормалью к пластине:"),
                          self.angle_edit)
        formLayout.addRow(self.tr("&Плотность материала пластины (лицевой)"),
                          self.pl_front_density_edit)
        formLayout.addRow(self.tr("&плотность материала пластины (тыльной)"),
                          self.pl_back_density_edit)
        formLayout.addRow(self.tr("&Динамический предел текучести материала "
                                  "пластины"), self.pl_lim_fluidity_edit)
        formLayout.addRow(self.tr("&Длина пластины"),
                          self.pl_length_edit)
        formLayout.addRow(self.tr("&Ширина пластины"),
                          self.pl_width_edit)
        # Добавляем поля ВВ
        formLayout.addRow(self.tr("&Толщина слоя ВВ"),
                          self.explosive_layer_height_edit)
        formLayout.addRow(self.tr("&Плотность ВВ"),
                          self.explosive_density_edit)
        formLayout.addRow(self.tr("&Скорость детонации заряда ВВ"),
                          self.detonation_velocity_edit)
        formLayout.addRow(self.tr("&Критический диаметр детонации ВВ"),
                          self.crit_dim_detonation_edit)
        formLayout.addRow(self.tr("&плотность материала КС"),
                          self.stream_density_edit)
        formLayout.addRow(self.tr("&динамический предел текучести материала "
                                  "КС"), self.stream_lim_fluidity_edit)

        formLayout.addRow(self.calculate_btn)



        # Добавляем toolbar на главное окно
        self.addToolBar(self.create_toolbar())
        self


        widget = QWidget()
        widget.setLayout(formLayout)
        self.setCentralWidget(widget)

        self.show()

    def create_toolbar(self):
        # self.toolbar = self.addToolBar('Exit')

        # Создаем объект toolbar
        toolbar = QToolBar('tools', self)

        # Кнопка выхода на toolbar
        exit_act = QAction(QIcon('icons/power.png'), 'Exit', self)
        # exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(QApplication.instance().quit)
        toolbar.addAction(exit_act)

        # Кнопка сохранения на toolbar
        save_act = QAction(QIcon('icons/floppy-disk.png'), 'Save', self)
        # save_act.setShortcut('Ctrl+S')
        # save_act.triggered.connect(QApplication.instance().quit)
        toolbar.addAction(save_act)

        # Кнопка загрузки файла на toolbar
        download_act = QAction(QIcon('icons/file.png'), 'Download', self)
        # save_act.setShortcut('Ctrl+D')
        # save_act.triggered.connect(QApplication.instance().quit)
        toolbar.addAction(download_act)

        # Кнопка импорта на toolbar
        import_act = QAction(QIcon('icons/import.png'), 'Import', self)
        # save_act.setShortcut('Ctrl+D')
        # save_act.triggered.connect(QApplication.instance().quit)
        toolbar.addAction(import_act)

        # toolbar.setAllowedAreas(QtCore.Qt.ToolBarArea.TopToolBarArea)

        # Запрещаем перемещать toolbar
        toolbar.setMovable(False)

        # Запрещаем скрывать toolbar
        toolbar.toggleViewAction().setVisible(False)
        return toolbar

    def calc_start(self):
        print("calc")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
