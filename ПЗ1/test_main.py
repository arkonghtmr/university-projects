import unittest
import math
from main import task_function


class TestCompositeFunction(unittest.TestCase):

    def test_values_subtest(self):
        """
        Проверка корректных значений с использованием subTest (цикл).
        """
        # Формат: (x, n, ожидаемый результат или 'check_calc')
        test_cases = [
            # Случай x < n (левая функция f(x) = 1/(x^2 - 9))
            (0, 5, -1 / 9),
            (2, 5, 1 / (4 - 9)),  # -0.2

            # Случай x == n (должен совпадать с f(n) из-за формулы стыковки)
            # g(n) - g(n) + f(n) == f(n)
            (5, 5, 1 / (25 - 9)),  # 1/16 = 0.0625

            # Случай x > n (правая функция со стыковкой)
            # Пусть n=4, x=21.
            # f(4) = 1/(16-9) = 1/7
            # g(4) = sqrt(19)
            # g(21) = sqrt(36) = 6
            # Res = 6 - sqrt(19) + 1/7
            (21, 4, 6 - math.sqrt(19) + 1 / 7)
        ]

        for x, n, expected in test_cases:
            with self.subTest(x=x, n=n):
                result = task_function(x, n)
                self.assertAlmostEqual(result, expected, places=7,
                                       msg=f"Ошибка при x={x}, n={n}")

    def test_singularities_left(self):
        """
        Тестирование чувствительных точек левой функции: x = 3, x = -3.
        f(x) = 1 / (x^2 - 9). Деление на ноль.
        """
        n = 10  # Граница справа, так что проверяем f(x)

        # Ожидаем ошибку деления на ноль
        with self.assertRaises(ZeroDivisionError):
            task_function(3, n)

        with self.assertRaises(ZeroDivisionError):
            task_function(-3, n)

    def test_singularities_boundary(self):
        """
        Тестирование ситуации, когда сама граница n вызывает ошибку.
        В формуле стыковки используется f(n). Если n=3, будет ошибка.
        """
        with self.assertRaises(ZeroDivisionError):
            # x=10, n=3. x >= n, считаем g(x) - g(n) + f(n). f(3) упадет.
            task_function(10, 3)

    def test_domain_error_right(self):
        """
        Тестирование области определения правой функции g(x) = sqrt(x + 15).
        x должно быть >= -15.
        """
        n = -20
        # Если x >= n, работает g(x). Возьмем x = -16 (это >= -20).
        # g(-16) = sqrt(-1) -> ValueError
        with self.assertRaises(ValueError):
            task_function(-16, n)

    def test_invalid_input_types(self):
        """
        Проверка реакции на некорректные типы данных (строки вместо чисел).
        Функция не проверяет типы, поэтому Python сам выбросит TypeError.
        """
        with self.assertRaises(TypeError):
            task_function("string", 5)

        with self.assertRaises(TypeError):
            task_function(10, "string")


if __name__ == "__main__":
    unittest.main()