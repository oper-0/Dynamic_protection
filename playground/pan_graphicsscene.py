import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self.right_mouse_pressed = False
        self.last_mouse_pos = None
        self.start_scene_rect = self.sceneRect()  # Начальные размеры сцены

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.right_mouse_pressed = True
            self.last_mouse_pos = event.pos()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.right_mouse_pressed = False
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.right_mouse_pressed:
            delta = event.pos() - self.last_mouse_pos
            self.last_mouse_pos = event.pos()

            # Изменяем размер сцены на основе направления движения мыши
            new_scene_rect = self.sceneRect().translated(-delta.x(), -delta.y())
            self.setSceneRect(new_scene_rect)

        super().mouseMoveEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = QGraphicsScene()
    view = CustomGraphicsView(scene)

    # Добавьте элементы QGraphicsItem на сцену (прямоугольники, круги и т. д.)
    # Пример:
    rect = QGraphicsRectItem(0, 0, 200, 200)
    rect.setBrush(QColor(255, 0, 0))  # Устанавливаем красный цвет для прямоугольника
    scene.addItem(rect)

    view.setWindowTitle("Перемещение правой кнопкой мыши с динамическим изменением размера сцены")
    view.setGeometry(100, 100, 800, 600)
    view.show()

    sys.exit(app.exec())
