import sys
from typing import List, Tuple


def min_coins_greedy(coins: List[int], amount: int) -> List[int]:
    """
    Находит минимальное количество монет для выдачи суммы amount
    с помощью жадного алгоритма.

    Предусловие: номиналы монет должны быть такими, чтобы жадный алгоритм давал оптимальный результат
    (например, стандартные валюты вроде [1, 5, 10, 25]).

    Args:
        coins: Доступные номиналы монет (положительные целые числа).
        amount: Сумма, которую нужно выдать (неотрицательное целое число).

    Returns:
        Список монет, составляющих сумму amount.
        Пустой список, если сумму выдать невозможно.
    """
    if amount == 0:
        return []

    sorted_coins = sorted(coins, reverse=True)
    result: List[int] = []
    remaining = amount

    for coin in sorted_coins:
        count = remaining // coin
        if count > 0:
            result.extend([coin] * count)
            remaining -= coin * count
        if remaining == 0:
            break

    if remaining > 0:
        print("Предупреждение: жадный алгоритм не смог выдать точную сумму.")

    return result


def prim_mst(graph: List[List[int]]) -> Tuple[List[Tuple[int, int, int]], int]:
    """
    Построение минимального остовного дерева (MST) с помощью алгоритма Прима.

    Args:
        graph: Матрица смежности. graph[u][v] — вес ребра между u и v.
               0 означает отсутствие ребра. Граф должен быть связным и неориентированным.

    Returns:
        Кортеж из:
        - Список рёбер MST: каждое ребро — (u, v, weight)
        - Суммарный вес MST
    """
    V = len(graph)
    if V == 0:
        return [], 0

    selected: List[bool] = [False] * V
    key: List[int] = [sys.maxsize] * V
    parent: List[int] = [-1] * V

    key[0] = 0
    mst_edges: List[Tuple[int, int, int]] = []
    total_weight = 0

    for _ in range(V):
        u = -1
        min_key = sys.maxsize
        for v in range(V):
            if not selected[v] and key[v] < min_key:
                min_key = key[v]
                u = v

        if u == -1:
            break  # Граф несвязный

        selected[u] = True
        total_weight += key[u]

        if parent[u] != -1:
            mst_edges.append((parent[u], u, graph[parent[u]][u]))

        for v in range(V):
            weight = graph[u][v]
            if weight > 0 and not selected[v] and weight < key[v]:
                key[v] = weight
                parent[v] = u

    return mst_edges, total_weight
