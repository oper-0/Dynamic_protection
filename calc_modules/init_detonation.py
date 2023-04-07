""" Модуль init_detonation рассчитывает время инициирования детонации в заряде
ВВ ЭДЗ

IMPORT
    math -- библиотека для расчета математических функций
    InData -- класс содержащий входные данные расчета

__autor__ = Tsib_4NR

__version__ = 1.0
"""

from math import cos, pi, sqrt
from objects.parametrs import InData


def _calc_inequality(data: InData) -> float:
    """Возвращает значение для неравенства для определения толщины слоя ВВ

    :param data: класс в котором хранятся входные данные расчета

    :rtype: float
    :return: значение выражения [м]
    """

    j5 = data.angle
    j14 = data.crit_dim_detonation
    j17 = data.stream_dim
    m16 = j17 / 1000
    m20 = j14 / 1000
    m5 = cos((j5 * pi) / 180)
    m21 = (m20 / 2) / ((1 - (m20 / 2)) / ((1 * m16) * m5))

    return m21


def _calc_pen_rate(data: InData) -> float:
    """Возвращает скорость проникновения кумулятивой струи

        :param data: класс в котором хранятся входные данные расчета

        :rtype: float
        :return: скорость проникновения струи [м/c]
    """
    # Получаем данные из класса InData
    # Плотность задаем в
    stream_density = data.stream_density * 1000
    pl_front_density = data.pl_front_density * 1000
    stream_velocity = data.stream_velocity * 1000

    lamb = sqrt(stream_density / pl_front_density)
    pen_speed = (lamb * stream_velocity) / (1 + lamb)

    return pen_speed


def do_main(data: InData) -> float:
    """Возвращает время инициирования детонации в заряде ВВ ЭДЗ

    :param data: класс в котором хранятся входные данные расчета

    :rtype: float
    :return: время инициирования детонации [с]
    """
    # Получаем данные из класса InData
    explosive_layer_height = data.explosive_layer_height

    # Задаем толщину ВВ в м
    explosive_height = explosive_layer_height / 1000
    # Вычисляем неравенство
    ineq = _calc_inequality(data)
    # Определяем время инициирования для тонкого слоя ВВ
    pen_rate = _calc_pen_rate(data)
    init_detonation_time = explosive_height / pen_rate

    # Если слой не тонкий или время инициирования ВВ меньше 1 мкс, то необходимо
    # пересчитать время для толстого слоя ВВ
    if not ((explosive_height >= ineq) and (init_detonation_time <= 1e-6)):
        detonation_velocity = data.detonation_velocity

        init_detonation_time = explosive_height / detonation_velocity

    return init_detonation_time
