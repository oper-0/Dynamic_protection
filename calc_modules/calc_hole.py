""" Модуль calc_hole рассчитывает значение отверстия кумулятивной струи
IMPORT
    math -- библиотека для расчета математических функций

__autor__ = Tsib_4NR

__version__ = 1.0
"""

import math as mt
from math import sqrt
from objects.parametrs import InData


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


def do_main(data: InData) -> float:
    j2 = data.coeff_nu
    j3 = data.pl_front_thickness
    j5 = data.angle
    j6 = data.pl_front_density
    j8 = data.pl_lim_fluidity
    j15 = data.stream_density
    j17 = data.stream_dim
    j18 = data.stream_velocity
    m2 = j3 / 1000
    m4 = (sqrt(_C_("Sheet1!M13") / _C_("Sheet1!M11")) / (
                1 + sqrt(_C_("Sheet1!M13") / _C_("Sheet1!M11")))) * _C_(
        "Sheet1!M17")
    Sheet1!M5: = cos((_C_("Sheet1!J5") * pi) / 180)
    Sheet1!M8: = (_C_("Sheet1!J2") * _C_("Sheet1!M2")) / (
                _C_("Sheet1!M4") * _C_("Sheet1!M5"))
    Sheet1!M9: = sqrt((_C_("Sheet1!M10") ** 2) - ((sqrt(
        (_C_("Sheet1!M10") ** 2) - (_C_("Sheet1!M16") ** 2)) - ((2 * _C_(
        "Sheet1!M8"))
                                                                * sqrt(
                _C_("Sheet1!M14") / _C_("Sheet1!M11")))) ** 2))
    Sheet1!M10: = (sqrt(_C_("Sheet1!M11") * _C_("Sheet1!M13")) / (
                sqrt(2 * _C_("Sheet1!M14")) * (
                    sqrt(_C_("Sheet1!M13")) + sqrt(_C_("Sheet1!M11")))))
    *(_C_("Sheet1!M16") * _C_("Sheet1!M17"))


    Sheet1!M11: = _C_("Sheet1!J6") * 1000
    Sheet1!M13: = _C_("Sheet1!J15") * 1000
    Sheet1!M14: = _C_("Sheet1!J8") * 1000000
    Sheet1!M16: = _C_("Sheet1!J17") / 1000
    Sheet1!M17: = _C_("Sheet1!J18") * 1000
    Sheet1!U4: = _C_("Sheet1!M9") * 1000
