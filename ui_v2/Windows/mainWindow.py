import os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QToolBar, QStatusBar, QDockWidget, QWidget, QLabel, QHBoxLayout, QSizePolicy, \
    QGraphicsScene, QTabWidget, QScrollArea

from playground.dragDrop import DropLabel
from ui_v2.ArmorItems_library.ERA import generate_catalog_shield, generate_catalog_shell
from ui_v2.infrastructure.Sceene import GraphicsScene, ControlView
from ui_v2.infrastructure.SceneObjects import SceneItemWidget
from ui_v2.infrastructure.UserLogger import LoggerWidget
from ui_v2.infrastructure.catalogWidget import SceneItemsCatalog
from ui_v2.infrastructure.helpers import ItemsCollection
from ui_v2.infrastructure.mulryTabDockArea import DockAreaWidget
from ui_v2.infrastructure.property_displayer import PropertyDisplayer
from ui_v2.interactor import INTERACTOR


class mainWindow(QMainWindow):

    def __init__(self, interactor: INTERACTOR):
        super().__init__()

        self.interactor = interactor

        self.TOOLBAR = None
        self.STATUSBAR = None
        self.MENUBAR = None
        self.LEFT_DOCK_AREA = None
        self.RIGHT_DOCK_AREA = None
        self.USER_LOGGER = LoggerWidget(QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'info_24.png')),
                                        QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'error_24.png')),
                                        QIcon(os.path.join(self.interactor.paths.abs_icons_dir, 'warn_24.png')),
                                        )
        self.ControlView = None
        self.PropertyDisplayer = PropertyDisplayer()
        self.ItemsCollection = ItemsCollection()  # Список всех объектов каталога. Для возможности дропа в ControlView

        self.setUpUi()

        # self.showMaximized()

        self.USER_LOGGER.log('Добро пожаловать!', 'info')

        self.show()

    def setUpUi(self):
        """
        Настраивает основное окно программы
        """
        self.setWindowTitle("Расчёт ДЗ")
        self.setWindowIcon(self.u_getQIcon('tortoise_1_64.png'))
        self.resize(1600, 800)
        # self._SetMenuBar()  # is it indeed needed?
        self._SetLeftDockArea()
        self._SetRightDockArea()
        self._SetBotDockArea()
        self._SetStatusBar()
        self._SetCentralWidget()  # must be initialized after _SetLeftDockArea 💩
        self._SetToolBar()
        self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)

    def _SetToolBar(self):
        """
        Настраивает ToolBar основного окна.
        Создает кнопки. Привязывает события.
        :return:
        """
        self.TOOLBAR = QToolBar()
        # self.TOOLBAR.setIconSize(QSize(32,32))
        self.TOOLBAR.setIconSize(QSize(48, 38))

        # tb_item_1 = QToolBarItem

        self.TOOLBAR.addAction(self.u_getQIcon('open-folder.png'), 'Открыть конфигурацию')
        self.TOOLBAR.actions()[-1].triggered.connect(lambda: self.USER_LOGGER.log('Not implemented yet', 'error'))

        self.TOOLBAR.addAction(self.u_getQIcon('diskette.png'), 'Сохранить конфигурацию')
        self.TOOLBAR.actions()[-1].triggered.connect(lambda: self.USER_LOGGER.log('Not implemented yet', 'error'))

        self.TOOLBAR.addAction(self.u_getQIcon('question.png'), 'Помощь')
        self.TOOLBAR.actions()[-1].triggered.connect(lambda: self.USER_LOGGER.log('Not implemented yet', 'error'))

        self.TOOLBAR.addAction(self.u_getQIcon('spellbook_64.png'), 'some function here')
        self.TOOLBAR.actions()[-1].triggered.connect(lambda: self.USER_LOGGER.log('Not implemented yet', 'error'))

        self.addToolBar(self.TOOLBAR)

    def _SetCentralWidget(self):

        self.ControlView = ControlView(self.ItemsCollection, self.USER_LOGGER.log, lambda msg: self.STATUS_BAR.showMessage(msg))

        # self.croll_are = QScrollArea()
        # self.croll_are.setWidget(self.ControlView)
        # self.setCentralWidget(self.croll_are)
        self.setCentralWidget(self.ControlView)

    def _SetBotDockArea(self):
        self.BOT_DOCK_AREA = QDockWidget()
        dockerWidget = DockAreaWidget(self.USER_LOGGER)

        layout = QHBoxLayout()

        layout.addWidget(dockerWidget)

        # dockerWidget = QWidget()
        self.BOT_DOCK_AREA.setWidget(dockerWidget)
        # dockerWidget.setLayout(layout)

        self.BOT_DOCK_AREA.setFloating(True)
        self.BOT_DOCK_AREA.setTitleBarWidget(QWidget(None))
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.BOT_DOCK_AREA)

        # self.splitDockWidget(self.LEFT_DOCK_AREA , self.BOT_DOCK_AREA, Qt.Orientation.Vertical)

    def _SetLeftDockArea(self):
        self.LEFT_DOCK_AREA = QDockWidget()

        left_dock_area_tabs = QTabWidget()
        # self.setStyleSheet("""QToolBar {background: rgb(30, 30, 30) }""")

        # lw = QLabel('ITEMS LIBRARY (IMPLEMENT ME!)') #fixme
        # ERA CATALOG
        shield_catalog_wgt = SceneItemsCatalog(column_count=2)
        catalog_items = generate_catalog_shield(self.interactor.paths.abs_img_dir, self.PropertyDisplayer.show_property_shield)
        # catalog_items = generate_catalog_shield(self.interactor.paths.abs_img_dir)
        for i in catalog_items:
            shield_catalog_wgt.add_item(i)
        test_itms = shield_catalog_wgt.test_populate_me(os.path.join(self.interactor.paths.abs_img_dir, 'question_mark_pink_500.png'))
        self.ItemsCollection.add(catalog_items)
        self.ItemsCollection.add(test_itms)
        left_dock_area_tabs.addTab(shield_catalog_wgt, 'Броня')
        # left_dock_area_tabs.tabBar()

        # SHELL CATALOG
        shell_catalog_wgt = SceneItemsCatalog(column_count=1)
        catalog_items = generate_catalog_shell(self.interactor.paths.abs_img_dir, self.PropertyDisplayer.show_property_shell)
        for i in catalog_items:
            shell_catalog_wgt.add_item(i)
        self.ItemsCollection.add(catalog_items)
        left_dock_area_tabs.addTab(shell_catalog_wgt, 'Снаряды')
        # left_dock_area_tabs.tabBar()

        # left_dock_area_tabs.addTab(QLabel('IMPLEMENT ME'), 'Снаряды')

        self.LEFT_DOCK_AREA.setWidget(left_dock_area_tabs)
        # self.LEFT_DOCK_AREA.setWidget(lw)
        self.LEFT_DOCK_AREA.setFloating(True)
        self.LEFT_DOCK_AREA.setTitleBarWidget(QWidget(None))
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.LEFT_DOCK_AREA)

    def _SetRightDockArea(self):
        self.RIGHT_DOCK_AREA = QDockWidget()

        # lw = QLabel('ITEM PROPERTY')  # fixme
        # lw = DropLabel2('ITEM PROPERTY') #fixme
        # lw = SceneItemsCatalog()
        # lw.test_populate_me(os.path.join(self.interactor.paths.abs_img_dir, 'question_mark_pink_500.png'))

        self.RIGHT_DOCK_AREA.setWidget(self.PropertyDisplayer)
        # self.RIGHT_DOCK_AREA.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.RIGHT_DOCK_AREA.setFloating(True)
        self.RIGHT_DOCK_AREA.setTitleBarWidget(QWidget(None))
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.RIGHT_DOCK_AREA)
        # self.RIGHT_DOCK_AREA.


    def _SetStatusBar(self):
        self.STATUS_BAR = QStatusBar()
        self.STATUS_BAR.showMessage('test caption') # TODO CHECKPOINT

        self.setStatusBar(self.STATUS_BAR)

    def u_getQIcon(self, ico_name: str) -> QIcon:
        return QIcon(os.path.join(self.interactor.paths.abs_icons_dir, ico_name))
