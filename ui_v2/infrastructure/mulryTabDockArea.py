from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget


class DockAreaWidget(QWidget):
    def __init__(self, *args):
        super().__init__()
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.West)

        tab0 = args[0]

        # for widgets in args:
        #     self.tabs.addTab()

        self.tabs.addTab(tab0, 'Logger')

        layout.addWidget(self.tabs)
        self.setLayout(layout)