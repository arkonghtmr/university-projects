import math

# ВАРИАНТ 25
def f(x):
    """
    чувствительные точки: x=3 и x=-3
    """
    return 1 / (x ** 2 - 9)


def g(x):
    """
    x должен быть больше или равен -15.
    """
    return math.sqrt(x + 15)


def task_function(x, n):
    """
    1. Проверка левой ветви (x < n)
    >>> round(task_function(0, 5), 5)
    -0.11111

    2. Проверка правой ветви и формулы стыковки (x >= n)
    >>> round(task_function(4, 4), 5)
    0.14286

    3. Проверка чувствительной точки (деление на ноль)
    >>> task_function(3, 5)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero
    """

    # Логика переключения
    if x < n:
        return f(x)
    else:
        return g(x) - g(n) + f(n)


# Запуск тестов
if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)