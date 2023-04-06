"""При прохождении тестов точность принимаем 5 знаков после запятой"""

import unittest
from objects.parametrs import InData

# Функции для тестов
from calc_modules import calc_hole
from calc_modules import init_detonation

FRACTIONAL_PART = 5


class MyTestCase(unittest.TestCase):
    def test_calc_hole_mod(self):
        data = InData(coeff_nu=4.5,
                      pl_front_thickness=1.5,
                      angle=68,
                      pl_front_density=7.85,
                      pl_lim_fluidity=500,
                      stream_density=8.96,
                      stream_dim=45,
                      stream_velocity=9)

        # Результат переводим в мм
        result = calc_hole.do_main(data) * 1e3
        self.assertAlmostEqual(result, 65.63410, places=FRACTIONAL_PART)

    def test_init_detonation_mod1(self):
        """Проверка случая толстой пластины"""
        data = InData(angle=68,
                      crit_dim_detonation=0.5,
                      stream_dim=45,
                      stream_density=8.96,
                      pl_front_density=7.85,
                      stream_velocity=9,
                      explosive_layer_height=10,
                      detonation_velocity=8000)

        # Результат переводим в мкс
        result = init_detonation.do_main(data) * 1e6
        self.assertAlmostEqual(result, 1.25000, places=FRACTIONAL_PART)

    def test_init_detonation_mod2(self):
        """Проверка случая тонкой пластины"""
        data = InData(angle=68,
                      crit_dim_detonation=0.5,
                      stream_dim=45,
                      stream_density=8.96,
                      pl_front_density=7.85,
                      stream_velocity=9,
                      explosive_layer_height=4,
                      detonation_velocity=8000)

        # Результат переводим в мкс
        result = init_detonation.do_main(data) * 1e6
        self.assertAlmostEqual(result, 0.86045, places=FRACTIONAL_PART)


if __name__ == '__main__':
    unittest.main()
