import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsItem, QMenu
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPainter


class CustomGraphicsItem(QGraphicsItem):
    def __init__(self):
        super().__init__()

    def boundingRect(self):
        return QRectF(-20, -20, 40, 40)  # Прямоугольник, описывающий границы элемента

    def paint(self, painter, option, widget):
        painter.drawEllipse(-20, -20, 40, 40)  # Рисование элемента

    def contextMenuEvent(self, event):
        menu = QMenu()

        action1 = menu.addAction("Действие 1")
        action2 = menu.addAction("Действие 2")

        # Обработчики действий
        action1.triggered.connect(self.action1_triggered)
        action2.triggered.connect(self.action2_triggered)

        menu.exec(event.screenPos())  # Отобразить контекстное меню в позиции щелчка

    def action1_triggered(self):
        print("Действие 1 выбрано")

    def action2_triggered(self):
        print("Действие 2 выбрано")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        view = QGraphicsView()
        scene = QGraphicsScene()
        item = CustomGraphicsItem()

        scene.addItem(item)
        view.setScene(scene)

        self.setCentralWidget(view)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Контекстное меню в PyQt6")
        self.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
