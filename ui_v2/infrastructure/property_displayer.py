import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QApplication, QMainWindow, QComboBox, QLabel, QCheckBox

from ui_v2.infrastructure.helpers import SceneObjProperty


class PropertyDisplayer(QWidget):
    def __init__(self):
        """
        Виджет для отображения свойств элемента сцены.
        """
        super().__init__()

        self.layout_0 = QVBoxLayout()

        self.layout_1_shell_props = QFormLayout()
        self.layout_1_shell_props_CONTAINER = QWidget()
        self.layout_1_shell_props_CONTAINER.setLayout(self.layout_1_shell_props)
        self.layout_1_shell_props_CONTAINER.setStyleSheet('background-color:darksalmon;')

        self.layout_1_shield_props = QFormLayout()
        self.layout_1_shield_props_CONTAINER = QWidget()
        self.layout_1_shield_props_CONTAINER.setLayout(self.layout_1_shield_props)
        self.layout_1_shield_props_CONTAINER.setStyleSheet('background-color:darkseagreen;')

        # self.layout_0.addLayout(self.layout_1_shell_props)
        self.layout_0.addWidget(self.layout_1_shell_props_CONTAINER)
        # self.layout_0.addLayout(self.layout_1_shield_props)
        self.layout_0.addWidget(self.layout_1_shield_props_CONTAINER)
        self.setLayout(self.layout_0)

        self.show()

    def show_property_shield(self, properties: list[SceneObjProperty]):
        """
        :param properties:
        :param type: 'shield' or 'shell'
        """
        # self.props_fields = []
        for r in range(self.layout_1_shield_props.rowCount()):
            self.layout_1_shield_props.removeRow(0)
        for p in properties:
            self.layout_1_shield_props.addRow(QLabel(p.key), p.widget)

    def show_property_shell(self, properties: list[SceneObjProperty]):
        """
        :param properties:
        :param type: 'shield' or 'shell'
        """
        # self.props_fields = []
        for r in range(self.layout_1_shell_props.rowCount()):
            self.layout_1_shell_props.removeRow(0)
        for p in properties:
            self.layout_1_shell_props.addRow(QLabel(p.key), p.widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QMainWindow()
    pd = PropertyDisplayer()
    w.setCentralWidget(pd)

    # dta = SceneObjProperty(key='Угол атаки',
    #                        start_value=60,
    #                        widget_type=QLabel())
    # dta.key = 'Угол атаки'
    # dta.start_value = '60'
    # dta.widget_type = QLabel

    dta = SceneObjProperty(key='Угол атаки', widget=QLabel('60'))
    dt2 = SceneObjProperty(key='yare yare daze', widget=QCheckBox())
    # dta = SceneObjProperty2(key='Угол атаки', widget=QLabel('60'))
    # dta = SceneObjProperty2(key='Угол атаки', widget=QLabel('60'))
    # dta = SceneObjProperty2(key='Угол атаки', widget=QLabel('60'))

    pd.show_shield_property([dta, dt2])
    w.show()
    sys.exit(app.exec())
