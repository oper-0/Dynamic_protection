# import math
# import matplotlib.pyplot as plt
# import numpy as np
#
# # Значения для угла наклона в градусах
# tilt_angle_degrees = np.arange(0, 360, 1)
#
# # Применяем формулу к каждому углу наклона
# length_values = 0.5 * tilt_angle_degrees + (0.5 * tilt_angle_degrees * np.cos(np.radians(tilt_angle_degrees)))
#
# # Создаем график
# plt.plot(tilt_angle_degrees, length_values, label='jet.length.value = 0.5 * jet.length.value + (0.5 * jet.length.value * cos(tilt_angle))')
#
# # Добавляем метки и легенду
# plt.xlabel('Угол наклона (градусы)')
# plt.ylabel('Значение jet.length.value')
# plt.legend()
#
# # Показываем график
# plt.show()

import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QMovie

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем макет
        layout = QVBoxLayout(self)

        # Создаем QLabel для отображения анимированного GIF
        self.gif_label = QLabel(self)
        layout.addWidget(self.gif_label)

        # Загружаем анимированный GIF
        movie = QMovie(r"C:\Users\4NR_Operator_34\Pictures\chris-lumain-3d.gif")
        self.gif_label.setMovie(movie)
        movie.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
