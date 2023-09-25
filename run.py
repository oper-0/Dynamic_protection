import os.path
import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication

from PyQt6.QtWidgets import QStyleFactory

# from qt_material import appl

from ui_v2.Windows.mainWindow import mainWindow
from ui_v2.interactor import INTERACTOR, path_keeper



interactor = INTERACTOR()

pk = path_keeper()
pk.abs_root_dir = os.getcwd()
pk.abs_icons_dir = os.path.join(pk.abs_root_dir, 'ui_v2', 'assets', 'icons')
pk.abs_img_dir = os.path.join(pk.abs_root_dir, 'ui_v2', 'assets', 'img')

interactor.paths = pk

app = QApplication(sys.argv)
app.setStyle('Fusion')
# ----------------------------------------------------------------
# file = QtCore.QFile("style.qss")
# file.open(QtCore.QFile.OpenModeFlag.ReadOnly | QtCore.QFile.OpenModeFlag.Text)
# stream = QtCore.QTextStream(file)
# app.setStyleSheet(stream.readAll())
# ----------------------------------------------------------------
w = mainWindow(interactor)
sys.exit(app.exec())