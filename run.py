import os.path
import sys

from PyQt6.QtWidgets import QApplication

from ui_v2.Windows.mainWindow import mainWindow
from ui_v2.interactor import INTERACTOR, path_keeper

interactor = INTERACTOR()

pk = path_keeper()
pk.abs_root_dir = os.getcwd()
pk.abs_icons_dir = os.path.join(pk.abs_root_dir, 'ui_v2', 'assets', 'icons')
pk.abs_img_dir = os.path.join(pk.abs_root_dir, 'ui_v2', 'assets', 'img')

interactor.paths = pk

app = QApplication(sys.argv)
w = mainWindow(interactor)
sys.exit(app.exec())