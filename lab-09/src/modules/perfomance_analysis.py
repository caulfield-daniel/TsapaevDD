import tracemalloc
import timeit
import random
from modules.dynamic_programming import (
    knapsack_01,
    fib_tabulation,
    lcs,
    levenshtein_distance,
)
import matplotlib.pyplot as plt
import os
from typing import Tuple, List


def measure_performance(func, *args) -> Tuple[float, float]:
    """
    Измеряет время выполнения и пиковое потребление памяти заданной функции.

    Запускает трассировку памяти и замер времени выполнения функции с указанными аргументами.
    Возвращает время в миллисекундах и память в килобайтах.

    Args:
        func (callable): Функция, производительность которой измеряется.
        *args: Аргументы, передаваемые в функцию.

    Returns:
        Tuple[float, float]: Кортеж из времени выполнения (мс) и пикового потребления памяти (КБ).
    """
    tracemalloc.start()
    start_time = timeit.default_timer()

    func(*args)

    end_time = timeit.default_timer()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    exec_time_ms = (end_time - start_time) * 1000
    memory_kb = peak / 1024  # перевод в КБ
    return exec_time_ms, memory_kb


def generate_items(capacity: int) -> Tuple[List[int], List[int]]:
    """
    Генерирует списки весов и стоимостей предметов для задачи о рюкзаке.

    Количество предметов: capacity * 10.
    Вес каждого предмета — случайное значение от 1 до capacity // 10 + 1.
    Стоимость — случайное значение от 1 до capacity * 10.

    Args:
        capacity (int): Максимальная ёмкость рюкзака.

    Returns:
        Tuple[List[int], List[int]]: Кортеж (список весов, список стоимостей).
    """
    weights = [random.randint(1, capacity // 10 + 1) for _ in range(capacity * 10)]
    values = [random.randint(1, capacity * 10) for _ in range(capacity * 10)]
    return weights, values


def generate_strings(length: int) -> Tuple[str, str]:
    """
    Генерирует две случайные строки заданной длины из заглавных латинских букв.

    Args:
        length (int): Длина каждой строки.

    Returns:
        Tuple[str, str]: Кортеж из двух случайных строк.
    """
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    str1 = ''.join(random.choice(letters) for _ in range(length))
    str2 = ''.join(random.choice(letters) for _ in range(length))
    return str1, str2


def visualize_performance(
    x_values: List[int],
    y_data: List[float],
    title: str,
    xlabel: str,
    ylabel: str,
    filename: str,
    label: str = "Algorithm",
    marker: str = "o"
) -> None:
    """
    Строит и сохраняет график зависимости производительности от входных данных.

    Создаёт линейный график с заданными параметрами, добавляет сетку, легенду и подписи.
    Автоматически создаёт директорию для файла, если она отсутствует.

    Args:
        x_values (List[int]): Значения по оси X (входные параметры).
        y_data (List[float]): Значения по оси Y (результаты измерений).
        title (str): Заголовок графика.
        xlabel (str): Подпись оси X.
        ylabel (str): Подпись оси Y.
        filename (str): Путь для сохранения графика.
        label (str): Название линии на графике. По умолчанию "Algorithm".
        marker (str): Стиль маркера точек. По умолчанию "o".
    """
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_data, label=label, marker=marker)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Создаём директорию, если она не существует
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.savefig(filename)
    plt.show()


# Knapsack
def visualization_knapsack(capacities: List[int]) -> None:
    """
    Анализирует и визуализирует производительность алгоритма knapsack_01.

    Измеряет время и память для различных ёмкостей рюкзака.

    Args:
        capacities (List[int]): Список значений ёмкости рюкзака.
    """
    times, memories = [], []
    for cap in capacities:
        weights, values = generate_items(cap)
        time, mem = measure_performance(knapsack_01, weights, values, cap)
        times.append(time)
        memories.append(mem)

    visualize_performance(
        capacities, times, "Время выполнения Knapsack 0/1 vs Capacity",
        "Capacity", "Время (ms)", "./report/knapsack_time.png", "Knapsack 0/1"
    )
    visualize_performance(
        capacities, memories, "Потребление памяти Knapsack 0/1 vs Capacity",
        "Capacity", "Память (КБ)", "./report/knapsack_memory.png", "Knapsack 0/1"
    )


# Fibonacci
def visualization_fib(n_values: List[int]) -> None:
    """
    Анализирует и визуализирует производительность алгоритма fib_tabulation.

    Измеряет время и память для различных значений n.

    Args:
        n_values (List[int]): Список значений n для вычисления чисел Фибоначчи.
    """
    times, memories = [], []
    for n in n_values:
        time, mem = measure_performance(fib_tabulation, n)
        times.append(time)
        memories.append(mem)

    visualize_performance(
        n_values, times, "Время выполнения Fibonacci Tabulation vs n",
        "n", "Время (ms)", "./report/fib_tabulation_time.png", "Fib Tabulation"
    )
    visualize_performance(
        n_values, memories, "Потребление памяти Fibonacci Tabulation vs n",
        "n", "Память (КБ)", "./report/fib_tabulation_memory.png", "Fib Tabulation"
    )


# LCS
def visualization_lcs(lengths: List[int]) -> None:
    """
    Анализирует и визуализирует производительность алгоритма lcs.

    Измеряет время и память для строк различной длины.

    Args:
        lengths (List[int]): Список длин строк.
    """
    times, memories = [], []
    for length in lengths:
        str1, str2 = generate_strings(length)
        time, mem = measure_performance(lcs, str1, str2)
        times.append(time)
        memories.append(mem)

    visualize_performance(
        lengths, times, "Время выполнения LCS vs Length",
        "Length", "Время (ms)", "./report/lcs_time.png", "LCS"
    )
    visualize_performance(
        lengths, memories, "Потребление памяти LCS vs Length",
        "Length", "Память (КБ)", "./report/lcs_memory.png", "LCS"
    )


# Levenshtein
def visualization_levenshtein(lengths: List[int]) -> None:
    """
    Анализирует и визуализирует производительность алгоритма levenshtein_distance.

    Измеряет время и память для строк различной длины.

    Args:
        lengths (List[int]): Список длин строк.
    """
    times, memories = [], []
    for length in lengths:
        str1, str2 = generate_strings(length)
        time, mem = measure_performance(levenshtein_distance, str1, str2)
        times.append(time)
        memories.append(mem)

    visualize_performance(
        lengths, times, "Время выполнения Levenshtein Distance vs Length",
        "Length", "Время (ms)", "./report/levenshtein_time.png", "Levenshtein Distance"
    )
    visualize_performance(
        lengths, memories, "Потребление памяти Levenshtein Distance vs Length",
        "Length", "Память (КБ)", "./report/levenshtein_memory.png", "Levenshtein Distance"
    )
