import math

def f(x):
    """
    Левая функция варианта 25: 1 / (x**2 - 9)
    """
    return 1 / (x**2 - 9)

def g(x):
    """
    Правая функция варианта 25: math.sqrt(x + 15)
    """
    return math.sqrt(x + 15)

def task_function(x, n):
    """
    Вычисляет значение составной функции.
    При x < n используется f(x).
    При x >= n используется формула стыковки: g(x) - g(n) + f(n).

    Аргументы:
    x -- число, аргумент функции
    n -- число, граница переключения функций

    Примеры (doctest):
    >>> task_function(0, 5) # x=0 < 5, используется f(0) = 1/(0-9) = -0.111...
    -0.1111111111111111

    >>> task_function(10, 5) # x=10 >= 5, стыковка. Проверим расчет:
    ... # f(5) = 1/16 = 0.0625
    ... # g(5) = sqrt(20) ~ 4.472
    ... # g(10) = sqrt(25) = 5.0
    ... # res = 5.0 - 4.4721359 + 0.0625 ~ 0.59036
    0.5903640516709852

    >>> task_function(3, 10) # x=3 < 10, f(3) -> деление на ноль
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero
    """
    if x < n:
        return f(x)
    else:
        # Формула стыковки
        return g(x) - g(n) + f(n)

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)