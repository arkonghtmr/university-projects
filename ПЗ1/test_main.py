import unittest
import math
from main import task_function


class TestCompositeFunction(unittest.TestCase):

    def test_values_subtest(self):
        """Проверка правильных вычислений через subTest"""
        test_cases = [
            (0, 5, -1 / 9),  # Левая ветвь
            (5, 5, 1 / 16),  # Сама граница
            (10, 4, 5 - math.sqrt(19) + (1 / 7))  # Правая ветвь
        ]


        for x, n, expected in test_cases:
            with self.subTest(x=x, n=n):
                result = task_function(x, n)
                self.assertAlmostEqual(result, expected, places=5)

    def test_zero_division_left(self):
        """Проверка деления на ноль в левой функции"""
        with self.assertRaises(ZeroDivisionError):
            task_function(3, 10)  # 3^2 - 9 = 0

        with self.assertRaises(ZeroDivisionError):
            task_function(-3, 10)  # (-3)^2 - 9 = 0

    def test_math_domain_error(self):
        """Проверка корня из отрицательного числа в правой функции"""
        with self.assertRaises(ValueError):
            # Под корнем будет -16 + 15 = -1. Это вызовет ValueError.
            task_function(-16, -20)

    # Этот метод проверяет некорректные данные
    def test_type_error(self):
        """Проверка передачи неверного типа данных"""
        with self.assertRaises(TypeError):
            task_function("текст", 5)


if __name__ == "__main__":
    unittest.main()