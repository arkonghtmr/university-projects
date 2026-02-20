import unittest
import math
from main import task_function


class TestCompositeFunction(unittest.TestCase):

    def test_values_subtest(self):
        """
        Проверка корректных значений с использованием subTest.
        """
        test_cases = [
            # (x, n, ожидаемое значение)
            # 1. Левая ветвь: x=0, n=5 -> f(0) = -1/9
            (0, 5, -1 / 9),

            # 2. Точка переключения: x=5, n=5 -> f(5) = 1/(25-9) = 1/16
            (5, 5, 0.0625),

            # 3. Правая ветвь: x=21, n=4.
            # f(4) = 1/7, g(4)=sqrt(19), g(21)=6
            # res = 6 - sqrt(19) + 1/7
            (21, 4, 6 - math.sqrt(19) + 1 / 7)
        ]

        for x, n, expected in test_cases:
            with self.subTest(x=x, n=n):
                result = task_function(x, n)
                self.assertAlmostEqual(result, expected, places=7,
                                       msg=f"Ошибка при x={x}, n={n}")

    def test_singularities(self):
        """
        Проверка точек разрыва (деление на ноль).
        f(x) имеет разрывы в 3 и -3.
        """
        n = 10  # n достаточно большое, чтобы мы попали в левую ветку

        with self.assertRaises(ZeroDivisionError):
            task_function(3, n)

        with self.assertRaises(ZeroDivisionError):
            task_function(-3, n)

    def test_domain_error(self):
        """
        Проверка области определения корня.
        g(x) = sqrt(x + 15). Ошибка, если x < -15.
        """
        n = -20  # n маленькое, чтобы мы попали в правую ветку

        # x = -16, это >= n, значит вызывается g(-16) -> sqrt(-1)
        with self.assertRaises(ValueError):
            task_function(-16, n)

    def test_invalid_input(self):
        """
        Проверка реакции на некорректные типы данных.
        """
        with self.assertRaises(TypeError):
            task_function("строка", 5)


if __name__ == "__main__":
    unittest.main()