""" Модуль calc_hole рассчитывает значение отверстия кумулятивной струи
IMPORT
    math -- библиотека для расчета математических функций

__autor__ = Tsib_4NR

__version__ = 1.0
"""

import math as mt
from math import sqrt


def calc_diam_inf(stream_diam, pl_dens, stream_dens,
                  pl_lim_fluidity, stream_speed):
    """Возвращает диаметр отверстия в полубесконечной приграде

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


def calc_max_hole(stream_diam_inf, stream_diam,
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


def calc_time_pen(coeff, pl_thick, pen_rate, angle):
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


def calc_pen_rate(pl_dens, stream_dens, stream_speed):
    """Возвращает скорость проникновения кумулятивой струи

    :param pl_dens: плотность материала пластины (лицевой) [кг/м3]
    :param stream_dens: плотность материала струи [кг/м3]
    :param stream_speed: скорость струи [м]

    :rtype: float
    :return: скорость проникновения струи [м]
    """
    lamb = sqrt(stream_dens / pl_dens)
    pen_speed = (lamb * stream_speed) / (1 + lamb)


def do_main(pl_dens, stream_dens, stream_speed, coeff_nu, pl_thickness, ):
    pen_speed_stream = calc_pen_rate()

    time_pen = calc_time_pen()

    return calc_max_hole()
