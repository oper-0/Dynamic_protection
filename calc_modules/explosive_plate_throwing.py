""" Модуль explosive_plate_throwing рассчитывает время разгона и максимальную
скорость пластины ДЗ. Также строит графики скорости, смещения и длины
пересекаемого пластиной участка

IMPORT
    math -- библиотека для расчета математических функций

__autor__ = Tsib_4NR

__version__ = 1.0
"""

from math import sqrt
from objects.parametrs import InData, DPPlate
from typing import Tuple
from enum import IntEnum, unique

@unique
class PlPositions(IntEnum):
    """Перечисление со значениями позиции пластин"""
    PL_FRONT = 1
    PL_BACK = 2

def _calc_asymmetric_pl_speed(data: InData) -> Tuple[float, float]:
    """Возвращает кортеж значений скоростей метания 1-ой и 2-ой пластин

        :param data: класс в котором хранятся входные данные расчета

        :rtype: Tuple[float, float]
        :return: кортеж скоростей метания пластин [скорость первой пластины,
            скорость второй пластины] [м/с]
    """
    front_load_factor = _calc_load_factor(data, PlPositions.PL_FRONT)
    back_load_factor = _calc_load_factor(data, PlPositions.PL_BACK)
    v14 = _calc_garni_energy(data)
    # Вычисляем скорость метания лицевой пластины
    speed_front_pl = sqrt(2 * v14) * \
                     sqrt((3 * front_load_factor) / (3 + front_load_factor + (((back_load_factor / front_load_factor) * ((front_load_factor + 2) / ((back_load_factor + 2) ** 2))) * (front_load_factor + 2 * back_load_factor + 6))))
    # Вычисляем скорость метания тыльной пластины
    speed_back_pl = (speed_front_pl * (back_load_factor / front_load_factor)) * ((front_load_factor + 2) / (back_load_factor + 2))

    # Проверяем значение коэффициента нагрузки. Если необходимо пересчитываем скорости
    if front_load_factor < 0.1:
        fr_w = _calc_blowing_param(data, speed_front_pl, speed_back_pl,
                                   PlPositions.PL_FRONT)
        speed_front_pl = speed_front_pl / fr_w
    if back_load_factor < 0.1:
        bk_w = _calc_blowing_param(data, speed_front_pl, speed_back_pl,
                                   PlPositions.PL_BACK)
        speed_back_pl = speed_back_pl / bk_w

    return speed_front_pl, speed_back_pl




def _calc_blowing_param(data: InData, pl_bk_speed, pl_fr_speed, pl_pos: PlPositions) -> float:
    """Возвращает параметр выдувания для пластины

    :param pl_bk_speed:
    :param pl_fr_speed:
    :param pl_pos:
    :param data:

    :rtype: float
    :return: Значение параметра выдувания пластины [б/р]
    """
    j9 = data.pl_length
    j10 = data.pl_width
    j20 = data.ksi_z
    j21 = data.ksi_r
    m18 = data.explosive_layer_height
    m19 = data.explosive_density
    m31 = data.pl_length
    m32 = data.pl_width

    m33 = j9 / j10
    # Вычисляем параметр формы
    form_param = (((m31 + m32) * m18) * m33) / (m31 * m32)

    fr_h = m18 * ((1 + (pl_bk_speed / pl_fr_speed)) ** -1)

    # Выбираем для какой пластины идет расчет
    if pl_pos == PlPositions.PL_FRONT:
        m2 = data.pl_front_thickness
        m11 = data.pl_front_density
        m29 = (m19 * fr_h) / (m11 * m2)
        w = sqrt(1 + (((1 + ((2 * j20) * m29)) / ((2 * j21) * m29)) * (form_param ** 2)))
    else:
        m3 = data.pl_back_thickness
        m12 = data.pl_back_density
        m28 = m18 - fr_h
        m30 = (m19 * m28) / (m12 * m3)
        w = sqrt(1 + (((1 + ((2 * j20) * m30)) / ((2 * j21) * m30)) * (form_param ** 2)))

    return w


def _calc_load_factor(data: InData, pl_pos: PlPositions) -> float:
    """Возвращает коэффициент нагрузки для пластины

        :param data: класс в котором хранятся входные данные расчета.
        :param pl_pos: положение пластины

        :rtype: float
        :return: Коэффициент нагрузки пластины [б/р]
    """
    # Определяем для какой пластины ведем расчет
    if pl_pos == PlPositions.PL_FRONT:
        pl_fr_thick = data.pl_front_thickness
        pl_bk_thick = data.pl_front_density
    else:
        pl_fr_thick = data.pl_back_thickness
        pl_bk_thick = data.pl_back_density

    j11 = data.explosive_layer_height
    j12 = data.explosive_density
    m2 = pl_fr_thick / 1000
    m11 = pl_bk_thick * 1000
    m18 = j11 / 1000
    m19 = j12 * 1000
    load_coeff = (m19 * m18) / (m11 * m2)
    """Можно подумать о генерации функции в зависимости от условий расчета. Считаем
    две пластины или одну"""

    return load_coeff

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


