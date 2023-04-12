""" Модуль explosive_plate_throwing рассчитывает время разгона и максимальную
скорость пластины ДЗ. Также строит графики скорости, смещения и длины
пересекаемого пластиной участка

IMPORT
    math -- библиотека для расчета математических функций

__autor__ = Tsib_4NR

__version__ = 1.0
"""

import math
from objects.parametrs import InData, DPPlate
from typing import Tuple

PL_FRONT = "front"
PL_BACK = "back"


def _calc_asymmetric_pl_speed(data: InData) -> Tuple[float, float]:
    """Возвращает кортеж значений скоростей метания 1-ой и 2-ой пластин

        :param data: класс в котором хранятся входные данные расчета

        :rtype: Tuple[float, float]
        :return: кортеж скоростей метания пластин [м/с] (нумерация по порядку)
    """



def _calc_load_factor(data: InData, pl_position: str) -> float:
    """Возвращает коэффициент нагрузки для пластины

        :param data: класс в котором хранятся входные данные расчета.
        :param pl_position: положение пластины

        :rtype: float
        :return: Коэффициент нагрузки пластины
    """
    # Определяем для какой пластины ведем расчет
    if pl_position == "front":
        j3 = data.pl_front_thickness
        j6 = data.pl_front_density
    else:
        j3 = data.pl_back_thickness
        j6 = data.pl_back_density

    j11 = data.explosive_layer_height
    j12 = data.explosive_density
    m2 = j3 / 1000
    m11 = j6 * 1000
    m18 = j11 / 1000
    m19 = j12 * 1000
    q16 = (m19 * m18) / (m11 * m2)

    return q16

def _calc_garni_energy(data: InData) -> float:
    # noinspection GrazieInspection
    """Возвращает значение энергии Гарни

        :param data:класс в котором хранятся входные данные расчета

        :rtype: float
        :return: Энергия Гарни [? какая-то стандартная единица]
        """
    j13 = data.detonation_velocity
    j19 = data.polytropy_index
    v14 = (j13 ** 2) / (2 * ((j19 ** 2) - 1))

    return v14


