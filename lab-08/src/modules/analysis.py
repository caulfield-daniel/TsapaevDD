from itertools import combinations
from modules.greedy_algorithms import fractional_knapsack


def greedy_discrete_knapsack(items, capacity):
    """Жадный алгоритм для дискретного рюкзака (0-1), без дробления предметов."""
    # Сортируем по убыванию удельной стоимости (ценность/вес)
    items_sorted = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
    total_value = 0
    total_weight = 0
    taken_items = []

    for value, weight in items_sorted:
        if total_weight + weight <= capacity:
            taken_items.append((value, weight))
            total_value += value
            total_weight += weight

    return total_value, taken_items


def knapsack_bruteforce(items, capacity):
    """Точный перебор для дискретного (0-1) рюкзака."""
    best_value = 0
    best_combo = []

    # Проверяем все возможные комбинации (включая пустую)
    for r in range(len(items) + 1):
        for combo in combinations(items, r):
            total_weight = sum(weight for _, weight in combo)
            total_value = sum(value for value, _ in combo)
            if total_weight <= capacity and total_value > best_value:
                best_value = total_value
                best_combo = combo

    return best_value, best_combo


def analysis():
    """
    Анализ и сравнение жадных алгоритмов и точного перебора для задачи о рюкзаке.
    Сравниваем:
    1. Жадный алгоритм для непрерывного рюкзака.
    2. Жадный алгоритм для дискретного (0-1) рюкзака.
    3. Точный перебор (оптимальное решение) для дискретного рюкзака.
    """
    # Данные для теста
    items = [(60, 10), (100, 20), (120, 30)]  # (стоимость, вес)
    capacity = 50

    # Выполнение алгоритмов
    frac_value = fractional_knapsack(items, capacity)
    greedy_value, greedy_combo = greedy_discrete_knapsack(items, capacity)
    brute_value, brute_combo = knapsack_bruteforce(items, capacity)

    # Форматированный вывод
    print(f"{'='*50}")
    print(f"АНАЛИЗ АЛГОРИТМОВ ДЛЯ ЗАДАЧИ О РЮКЗАКЕ")
    print(f"{'='*50}")
    print(f"Ёмкость рюкзака: {capacity}")
    print(f"Предметы (стоимость, вес): {items}")
    print(f"-" * 50)
    print(f"Жадный (непрерывный рюкзак):     {frac_value:.2f}")
    print(f"Жадный (дискретный 0-1):         {greedy_value}, выбранные: {greedy_combo}")
    print(f"Точный перебор (0-1):            {brute_value}, выбранные: {brute_combo}")
    print(f"-" * 50)
    print(f"Жадный (дискретный) эффективность: {greedy_value / brute_value:.2%}")
    if frac_value > 0:
        print(f"Жадный (непрерывный) эффективность: {brute_value / frac_value:.2%}")
