import matplotlib.pyplot as plt
import numpy as np
from main import task_function


def plot_graphs():
    # Создаем диапазон значений x от -16 до 10
    x_values = np.linspace(-16, 10, 500)

    # Два случая для n:
    # 1. n = 0 (разрывы f(x) в правой части не учитываются, т.к. там работает g(x))
    # 2. n = 4 (разрывы f(x) видны, так как 3 < 4)
    n_options = [0, 4]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for i, n in enumerate(n_options):
        y_values = []
        for x in x_values:
            try:
                # Отсеиваем точки разрыва для красоты графика
                if abs(x - 3) < 0.1 or abs(x + 3) < 0.1:
                    y_values.append(np.nan)
                else:
                    y_values.append(task_function(x, n))
            except (ValueError, ZeroDivisionError):
                y_values.append(np.nan)

        ax = axes[i]
        ax.plot(x_values, y_values, label=f'Функция (n={n})', color='blue', linewidth=2)

        # Рисуем вертикальную линию границы n
        ax.axvline(x=n, color='red', linestyle='--', label=f'Граница n={n}')

        ax.set_title(f'График при n = {n}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True)
        ax.legend()

        # Ограничиваем ось Y, чтобы график не "улетал" в бесконечность в точках разрыва
        ax.set_ylim(-10, 10)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_graphs()