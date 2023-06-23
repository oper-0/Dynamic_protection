import os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QToolBar, QStatusBar, QDockWidget, QWidget, QLabel, QHBoxLayout, QSizePolicy

from ui_v2.ArmorItems_library.ERA import generate_catalog
from ui_v2.infrastructure.Sceene import Scene
from ui_v2.infrastructure.SceneObjects import SceneItemWidget
from ui_v2.infrastructure.UserLogger import LoggerWidget
from ui_v2.infrastructure.catalogWidget import SceneItemsCatalog
from ui_v2.infrastructure.mulryTabDockArea import DockAreaWidget
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
        self.SCENE = None

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
        self._SetToolBar()
        # self._SetMenuBar()  # is it indeed needed?
        self._SetLeftDockArea()
        self._SetRightDockArea()
        self._SetCentralWidget()
        self._SetBotDockArea()
        self._SetStatusBar()

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
        self.TOOLBAR.addAction(self.u_getQIcon('spellbook_64.png'), 'some function here')
        self.TOOLBAR.actions()[-1].triggered.connect(lambda: print('yareyare'))

        self.addToolBar(self.TOOLBAR)

    def _SetCentralWidget(self):
        self.SCENE = Scene()

        self.setCentralWidget(self.SCENE)

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

    def _SetLeftDockArea(self):
        self.LEFT_DOCK_AREA = QDockWidget()

        # lw = QLabel('ITEMS LIBRARY (IMPLEMENT ME!)') #fixme
        lw = SceneItemsCatalog()
        catalog_items = generate_catalog(self.interactor.paths.abs_img_dir)
        for i in catalog_items:
            lw.add_item(i)

        # lw.add_item(SceneItemWidget('ДЗ', 'Динамическая Защита', os.path.join(self.interactor.paths.abs_img_dir, 'ERA_shell_1.png')))
        # lw.add_item(SceneItemWidget('ЭДЗ', 'Элемент Динамической Защиты', os.path.join(self.interactor.paths.abs_img_dir, 'ERA_3.png')))
        # lw.add_item(SceneItemWidget('Резина', 'Резиновый брусок ???', os.path.join(self.interactor.paths.abs_img_dir, 'rubber_bar.png')))
        lw.test_populate_me(os.path.join(self.interactor.paths.abs_img_dir, 'question_mark_pink_500.png'))

        self.LEFT_DOCK_AREA.setWidget(lw)
        self.LEFT_DOCK_AREA.setFloating(True)
        self.LEFT_DOCK_AREA.setTitleBarWidget(QWidget(None))
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.LEFT_DOCK_AREA)

    def _SetRightDockArea(self):
        self.RIGHT_DOCK_AREA = QDockWidget()

        lw = QLabel('ITEM PROPERTY') #fixme
        # lw = SceneItemsCatalog()
        # lw.test_populate_me(os.path.join(self.interactor.paths.abs_img_dir, 'question_mark_pink_500.png'))

        self.RIGHT_DOCK_AREA.setWidget(lw)
        # self.RIGHT_DOCK_AREA.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.RIGHT_DOCK_AREA.setFloating(True)
        self.RIGHT_DOCK_AREA.setTitleBarWidget(QWidget(None))
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.RIGHT_DOCK_AREA)

    def _SetStatusBar(self):
        self.STATUS_BAR = QStatusBar()
        self.STATUS_BAR.showMessage('test text (DELETE ME!)')

        self.setStatusBar(self.STATUS_BAR)

    def u_getQIcon(self, ico_name: str) -> QIcon:
        return QIcon(os.path.join(self.interactor.paths.abs_icons_dir, ico_name))
