""" Модуль calc_hole рассчитывает значение отверстия кумулятивной струи
IMPORT
    math -- библиотека для расчета математических функций

__autor__ = Tsib_4NR

__version__ = 1.1
"""

import math as mt
from math import sqrt, cos
from objects.parametrs import InData


def _calc_diam_inf(stream_diam, pl_dens, stream_dens,
                  pl_lim_fluidity, stream_speed):
    """Возвращает диаметр отверстия в полубесконечной приграде [м]

    :param stream_diam: диаметр струи [м]
    :param pl_dens: плотность материала пластины (лицевой) [кг/м3]
    :param stream_dens: плотность материала струи [кг/м3]
    :param pl_lim_fluidity: динамический предел текучести материала
        пластины [Па]
    :param stream_speed: скорость струи [м/м]

    :rtype: float
    :return: диаметр отверстия [м]
    """
    a = sqrt(stream_dens * pl_dens)
    b = sqrt(2 * pl_lim_fluidity) * (sqrt(pl_dens) * sqrt(stream_dens))
    inf_dim_hole = (a / b) * stream_diam * stream_speed

    return inf_dim_hole


def _calc_max_hole(stream_diam_inf, stream_diam,
                  time_pen, pl_lim_fluidity, pl_dens):
    """Возвращает максимальный диаметр отверстия в пластине [м]

    :param stream_diam_inf: диаметр отверстия в полубесконечной пластине [м]
    :param stream_diam: диаметр струи [м]
    :param time_pen: время пробития пластины [с]
    :param pl_lim_fluidity: динамический предел текучести материала
        пластины [Па]
    :param pl_dens: плотность материала пластины (лицевой) [кг/м3]

    :rtype: float
    :return: максимальный диаметр отверстия [м]
    """
    a = sqrt(stream_diam_inf**2 - stream_diam**2)
    b = 2 * time_pen * sqrt(pl_lim_fluidity / pl_dens)
    max_hole_dim = sqrt(stream_diam_inf ** 2 - (a - b) ** 2)

    return max_hole_dim


def _calc_time_pen(coeff, pl_thick, pen_rate, angle):
    """Возвращает время пробития пластины [с]

    :param coeff: эмпирический коэффициент [б/р]
    :param pl_thick:  толщина пластины [м]
    :param pen_rate: скорость проникновения струи [м/с]
    :param angle: угол между струей и нормалью к пластине [градусы]

    :rtype: float
    :return: время пробития пластины [с]
    """
    cos_angle = mt.cos(mt.radians(angle))
    pen_time = (coeff * pl_thick) / (pen_rate * cos_angle)

    return pen_time


def _calc_pen_rate(pl_dens, stream_dens, stream_speed):
    """Возвращает скорость проникновения кумулятивой струи

    :param pl_dens: плотность материала пластины (лицевой) [кг/м3]
    :param stream_dens: плотность материала струи [кг/м3]
    :param stream_speed: скорость струи [м]

    :rtype: float
    :return: скорость проникновения струи [м/c]
    """
    lamb = sqrt(stream_dens / pl_dens)
    pen_speed = (lamb * stream_speed) / (1 + lamb)

    return pen_speed


def do_main(data: InData) -> float:
    """Главная функция. Рассчитывает диаметр отверстия в пластине. Остальные
    функции по факту не нужны!

    :param data: класс в котором хранятся входные данные расчета

    :rtype: float
    :return: диаметр отверстия в пластине [м]
    """

    j2 = data.coeff_nu
    j3 = data.pl_front_thickness
    j5 = data.angle
    j6 = data.pl_front_density
    j8 = data.pl_lim_fluidity
    j15 = data.stream_density
    j17 = data.stream_dim
    j18 = data.stream_velocity

    m11 = j6 * 1000
    m13 = j15 * 1000
    m14 = j8 * 1e6
    m16 = j17 / 1000
    m17 = j18 * 1000

    m2 = j3 / 1000
    m4 = (sqrt(m13 / m11) / (1 + sqrt(m13 / m11))) * m17
    m5 = cos((j5 * mt.pi) / 180)
    m8 = (j2 * m2) / (m4 * m5)
    m10 = (sqrt(m11 * m13) / (sqrt(2 * m14) * (sqrt(m13) + sqrt(m11)))) * (m16 * m17)
    m9 = sqrt((m10 ** 2) - ((sqrt((m10 ** 2) - (m16 ** 2)) - ((2 * m8) * sqrt(m14 / m11))) ** 2))

    return m9