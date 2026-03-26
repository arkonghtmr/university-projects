import matplotlib.pyplot as plt
import numpy as np
from main import task_function


def safe_compute(x, n):
    """Безопасная обертка для графика."""

    if abs(x - 3) < 0.1 or abs(x + 3) < 0.1:
        return np.nan

    try:
        return task_function(x, n)
    except (ValueError, ZeroDivisionError):
        return np.nan


def plot_graphs():
    x_values = np.linspace(-16, 10, 500)

    # Требование задания: Построить два графика для разных n
    n_options = [0, 4]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for i, n in enumerate(n_options):
        y_values = [safe_compute(x, n) for x in x_values]

        ax = axes[i]
        ax.plot(x_values, y_values, label=f'Функция (n={n})', color='blue')

        ax.axvline(x=n, color='red', linestyle='--', label=f'Граница n={n}')

        ax.set_title(f'График при n = {n}')
        ax.set_xlabel('Ось X')
        ax.set_ylabel('Ось Y')
        ax.set_ylim(-10, 10)
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_graphs()