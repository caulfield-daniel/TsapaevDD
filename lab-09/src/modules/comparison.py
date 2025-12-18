import timeit
import os
import tracemalloc
import matplotlib.pyplot as plt
from typing import List, Tuple, Callable
from modules.dynamic_programming import fib_memo, fib_tabulation
from modules.dynamic_programming import knapsack_01_with_items


def measure_performance(func: Callable, *args) -> Tuple[float, float]:
    """
    Измеряет время выполнения и пиковое потребление памяти функции.

    Args:
        func (Callable): Функция для измерения.
        *args: Аргументы, передаваемые в функцию.

    Returns:
        Tuple[float, float]: Время выполнения (мс) и память (КБ).
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


def compare_fibonacci_algorithms(n_values: List[int]) -> None:
    """
    Сравнивает производительность алгоритмов Фибоначчи:
    - С мемоизацией (top-down)
    - С табуляцией (bottom-up)

    Строит графики времени и памяти, выводит данные в консоль.

    Args:
        n_values (List[int]): Список значений n для анализа.
    """
    memo_times, memo_mem = [], []
    tabu_times, tabu_mem = [], []

    for n in n_values:
        # Измерение для fib_memo
        t1, m1 = measure_performance(fib_memo, n)
        memo_times.append(t1)
        memo_mem.append(m1)

        # Измерение для fib_tabulation
        t2, m2 = measure_performance(fib_tabulation, n)
        tabu_times.append(t2)
        tabu_mem.append(m2)

    # Вывод в консоль
    print("Время выполнения (Top-Down):", memo_times)
    print("Время выполнения (Bottom-Up):", tabu_times)
    print("Память (Top-Down):", memo_mem)
    print("Память (Bottom-Up):", tabu_mem)

    # Построение графиков
    plt.figure(figsize=(12, 5))

    # Время выполнения
    plt.subplot(1, 2, 1)
    plt.plot(n_values, memo_times, label="Top-Down (Memoization)", marker="o")
    plt.plot(n_values, tabu_times, label="Bottom-Up (Tabulation)", marker="o")
    plt.title("Время выполнения Фибоначчи vs n")
    plt.xlabel("n")
    plt.ylabel("Время (мс)")
    plt.legend()
    plt.grid(True)

    # Потребление памяти
    plt.subplot(1, 2, 2)
    plt.plot(n_values, memo_mem, label="Top-Down (Memoization)", marker="o")
    plt.plot(n_values, tabu_mem, label="Bottom-Up (Tabulation)", marker="o")
    plt.title("Потребление памяти Фибоначчи vs n")
    plt.xlabel("n")
    plt.ylabel("Память (КБ)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    os.makedirs("./report", exist_ok=True)
    plt.savefig("./report/fib_analysis.png")
    plt.show()


def greedy_discrete_knapsack(
    items: List[Tuple[int, int]], capacity: int
) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Жадный алгоритм для задачи 0-1 рюкзака.

    Сортирует предметы по убыванию стоимости на единицу веса.
    Добавляет предметы, если они помещаются целиком.

    Args:
        items (List[Tuple[int, int]]): Список кортежей (стоимость, вес).
        capacity (int): Максимальная ёмкость рюкзака.

    Returns:
        Tuple[int, List[Tuple[int, int]]]: Общая стоимость и список взятых предметов.
    """
    # Сортировка по удельной стоимости (стоимость/вес) в порядке убывания
    sorted_items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)

    total_value = 0
    taken_items = []
    remaining_capacity = capacity

    for value, weight in sorted_items:
        if weight <= remaining_capacity:
            total_value += value
            taken_items.append((value, weight))
            remaining_capacity -= weight

    return total_value, taken_items


def analyze_knapsack_algorithms() -> None:
    """
    Сравнивает жадный алгоритм и динамическое программирование
    для задачи 0-1 рюкзака.

    Выводит результаты обоих подходов: общую стоимость и выбранные предметы.
    """
    # Данные для теста
    items = [(60, 10), (100, 20), (120, 30)]
    weights = [item[1] for item in items]
    values = [item[0] for item in items]
    capacity = 50

    # Жадный алгоритм
    greedy_value, greedy_combo = greedy_discrete_knapsack(items, capacity)

    # Динамическое программирование
    dp_value, dp_combo = knapsack_01_with_items(weights, values, capacity)

    # Вывод результатов
    print(f"Рюкзак ёмкостью: {capacity}")
    print(f"Предметы (стоимость, вес): {items}")
    print(f"Жадный алгоритм: стоимость = {greedy_value}, набор = {greedy_combo}")
    print(f"ДП (оптимальное решение): стоимость = {dp_value}, набор = {dp_combo}")

    # Рекомендация
    if dp_value > greedy_value:
        print("ДП находит более оптимальное решение.")
    elif dp_value == greedy_value:
        print("Жадный алгоритм нашёл оптимальное решение.")
    else:
        print("Внимание: жадный алгоритм превзошёл ДП — проверьте реализацию.")


def run_analysis() -> None:
    """
    Основная точка входа для запуска всех анализов.
    """
    # Сравнение алгоритмов Фибоначчи
    n_values = list(range(10, 101, 10))
    compare_fibonacci_algorithms(n_values)

    # Сравнение алгоритмов рюкзака
    analyze_knapsack_algorithms()
