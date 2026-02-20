import matplotlib.pyplot as plt
import numpy as np
from main import task_function


def plot_graphs():
    # Создаем диапазон значений x
    # f(x) имеет разрывы в 3 и -3, g(x) определена от -15
    # Возьмем диапазон от -14 до 10, чтобы показать интересные места
    x = np.linspace(-14, 10, 400)

    # Два варианта n для демонстрации
    n_values = [0, 4]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for i, n in enumerate(n_values):
        y = []
        for val in x:
            try:
                # Обработка точек разрыва для чистоты графика
                if abs(val - 3) < 0.1 or abs(val + 3) < 0.1:
                    y.append(np.nan)
                else:
                    y.append(task_function(val, n))
            except (ValueError, ZeroDivisionError):
                y.append(np.nan)

        ax = axes[i]
        ax.plot(x, y, label=f'Сдвоенная функция (n={n})', color='blue')

        # Добавим визуальную линию границы n
        ax.axvline(x=n, color='red', linestyle='--', label=f'Граница n={n}')

        ax.set_title(f'График функции при n = {n}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True)
        ax.legend()

        # Ограничим Y, чтобы асимптоты не сжимали график
        ax.set_ylim(-10, 10)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_graphs()