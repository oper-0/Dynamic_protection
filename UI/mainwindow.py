# -*- coding: utf-8 -*-

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QToolBar, \
    QVBoxLayout, QLabel, QFormLayout, QLineEdit, QWidget, QScrollBar, \
    QScrollArea


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        # Задаем константы
        self.MIN_WIDTH_WINDOW = 470

        self.initUI()

    def initUI(self):
        self.calculate_btn = QPushButton("Рассчитать")
        self.calculate_btn.pressed.connect(self.calc_start)

        self.statusBar().showMessage("StatusBar")

        #  Параметры окна
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle("Расчет ДЗ")
        self.setWindowIcon(QIcon("icons/star.png"))
        self.setMinimumWidth(self.MIN_WIDTH_WINDOW)

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

        # Создаем форму ввода данных
        form_layout = QFormLayout()

        # Добавляем поля ввода в часть форму.
        # Добавляем поля пластины
        form_layout.addRow(self.tr("&Эмпирический коэффициент:"),
                           self.coeff_nu_edit)
        form_layout.addRow(self.tr("&Толщина пластины (лицевой):"),
                           self.pl_front_thickness_edit)
        form_layout.addRow(self.tr("&Толщина пластины (тыльной):"),
                           self.pl_back_thickness_edit)
        form_layout.addRow(self.tr("&Угол между КС и нормалью к пластине:"),
                           self.angle_edit)
        form_layout.addRow(self.tr("&Плотность материала пластины (лицевой)"),
                           self.pl_front_density_edit)
        form_layout.addRow(self.tr("&плотность материала пластины (тыльной)"),
                           self.pl_back_density_edit)
        form_layout.addRow(self.tr("&Динамический предел текучести материала пластины"),
                           self.pl_lim_fluidity_edit)
        form_layout.addRow(self.tr("&Длина пластины"),
                           self.pl_length_edit)
        form_layout.addRow(self.tr("&Ширина пластины"),
                           self.pl_width_edit)

        # Добавляем поля ВВ
        form_layout.addRow(self.tr("&Толщина слоя ВВ"),
                           self.explosive_layer_height_edit)
        form_layout.addRow(self.tr("&Плотность ВВ"),
                           self.explosive_density_edit)
        form_layout.addRow(self.tr("&Скорость детонации заряда ВВ"),
                           self.detonation_velocity_edit)
        form_layout.addRow(self.tr("&Критический диаметр детонации ВВ"),
                           self.crit_dim_detonation_edit)
        # Добавляем поля струи
        form_layout.addRow(self.tr("&плотность материала КС"),
                           self.stream_density_edit)
        form_layout.addRow(self.tr("&динамический предел текучести материала""КС"),
                           self.stream_lim_fluidity_edit)
        form_layout.addRow(self.tr("&диаметр КС"),
                           self.stream_dim_edit)
        form_layout.addRow(self.tr("&скорость КС"),
                           self.stream_velocity_edit)

        # Добавляем остальные параметры
        form_layout.addRow(self.tr("&Показатель политропы продуктов детонации"),
                           self.polytropy_index_edit)
        form_layout.addRow(self.tr("&Давление детонации"),
                           self.detonation_pressure_edit)

        # Устанавливаем заголовок для двух общих параметров кси
        form_layout.addRow(QLabel("Параметры, определяющие распределение скоростей продуктов детонации:"))
        form_layout.addRow(self.tr("\u03BEz"), self.ksi_z_edit)
        form_layout.addRow(self.tr("\u03BEr"), self.ksi_r_edit)
        form_layout.addRow(self.tr("&Коэффициент для среднего давления"),
                           self.coeff_avr_pressure_edit)
        form_layout.addRow(self.tr("&Коэффициент увеличения диаметра КС"),
                           self.coeff_stream_dim_extension_edit)

        # Устанавливаем выравнивание подписей полей по правому краю
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Создаем область прокрутки формы
        form_scroll_area = QScrollArea()
        form_scroll_area.setWidgetResizable(True)
        form_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Добавляем верхнюю часть формы во внешний контейнер
        # main_layout.addLayout(form_layout)

        # Инструкция устанавливает все подписи над полями заполнения
        # (висит для справки)
        # formLayout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)

        # Создаем нижнюю часть формы

        # Добавляем верхнюю часть формы во внешний контейнер
        # main_layout.addLayout(bottom_form_layout)

        # Ограничиваем растяжение форм при помощи растягиваемого контейнера
        # снизу всех форм ввода
        # main_layout.addStretch()

        # Устанавливаем форму на главное окно
        widget = QWidget()
        widget.setLayout(form_layout)
        form_scroll_area.setWidget(widget)
        self.setCentralWidget(form_scroll_area)

        # Добавляем toolbar на главное окно
        self.addToolBar(self.create_toolbar())

        self.show()

    def create_joint_label_form(self, head_name: str,
                                *par_names: str) -> QVBoxLayout:
        """Принимает заголовок формы и ее элементы.
        Возвращает контейнер QVBoxLayout со всеми переданными компонентами
        """
        container = QVBoxLayout()
        # container.addStretch()

        heading = QLabel(head_name)
        container.addWidget(heading)

        bottom_form = QFormLayout()
        for par_name in par_names:
            bottom_form.addRow(self.tr(f'&{par_name}'), QLineEdit())
        container.addLayout(bottom_form)

        return container


    def create_toolbar(self) -> QToolBar:
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
