from PyQt6.QtWidgets import QWidget, QGridLayout, QScrollArea, QVBoxLayout, QSizePolicy, QListWidget

from ui_v2.infrastructure.SceneObjects import SceneItemWidget
from ui_v2.infrastructure.Spacers import VSpacer


class SceneItemsCatalog(QWidget):

    def __init__(self, column_count: int = 2):
        super().__init__()
        self.main_layout = QVBoxLayout()

        self.layoutGrid = QGridLayout()
        self.layoutGrid.setContentsMargins(0, 0, 0, 0)
        self.layoutGrid.setSpacing(0)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
        scrollArea.horizontalScrollBar().hide()
        scrollArea.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
        scrollArea.verticalScrollBar().hide()
        widget_for_scroll_area = QWidget()
        widget_for_scroll_area.setLayout(self.layoutGrid)
        scrollArea.setWidget(widget_for_scroll_area)

        self.max_columns = column_count-1

        self.cur_col = 0
        self.cur_row = 0

        self.spacer = VSpacer()

        self.main_layout.addWidget(scrollArea)
        self.setLayout(self.main_layout)


        # self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)


    def add_item(self, sceneIt: SceneItemWidget):
        self.remove_spacer()
        self.layoutGrid.addWidget(sceneIt, self.cur_row, self.cur_col)
        self.update_pos()
        self.add_spacer()

    def clear_items(self): ...

    def update_pos(self):
        if self.cur_col >= self.max_columns:
            self.cur_col = 0
            self.cur_row += 1
            return
        self.cur_col += 1

    def test_populate_me(self, img_path: str):
        items_count = 50
        itms = []
        for i in range(items_count):
            itm = SceneItemWidget('test_itm-{}'.format(i), 'this is test item made for debug use', img_path)
            self.add_item(itm)
            itms.append(itm)
        return itms

    def add_spacer(self):
        self.layoutGrid.addWidget(self.spacer)

    def remove_spacer(self):
        self.layoutGrid.removeWidget(self.spacer)
