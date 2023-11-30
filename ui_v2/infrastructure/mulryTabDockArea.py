from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from ui_v2.infrastructure.calc_result_displayer import DisplayerProtocol


class DockAreaWidget(QWidget):
    def __init__(self, logger, calc_displayer: DisplayerProtocol):
        super().__init__()
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.West)

        # tab0 = args[0]

        # for key, tab in kwargs.items():
        #     self.tabs.addTab(tab, key)

        # for widgets in args:
        #     self.tabs.addTab()

        self.tabs.addTab(logger, 'Журнал')
        self.tabs.addTab(calc_displayer, 'Расчёт')

        layout.addWidget(self.tabs)
        self.setLayout(layout)