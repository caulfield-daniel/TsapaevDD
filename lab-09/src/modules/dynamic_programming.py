from typing import List, Tuple, Dict, Optional


def fib_naive(n: int) -> int:
    """
    Возвращает n-е число Фибоначчи с использованием наивной рекурсии.

    Алгоритм напрямую следует определению:
    F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2).h

    Args:
        n (int): Позиция числа Фибоначчи (неотрицательное целое).

    Returns:
        int: n-е число Фибоначчи.

    Временная сложность: O(2^n)
    Пространственная сложность: O(n) — из-за глубины стека вызовов.
    """
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n: int, memo: Optional[Dict[int, int]] = None) -> int:
    """
    Возвращает n-е число Фибоначчи с мемоизацией (рекурсивный top-down подход).

    Использует словарь для кэширования уже вычисленных значений.

    Args:
        n (int): Позиция числа Фибоначчи.
        memo (Dict[int, int], опционально): Словарь для хранения результатов.

    Returns:
        int: n-е число Фибоначчи.

    Временная сложность: O(n)
    Пространственная сложность: O(n) — для кэша и стека вызовов.
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def fib_tabulation(n: int) -> int:
    """
    Возвращает n-е число Фибоначчи с использованием итеративной таблицы (bottom-up).

    Строит массив значений от 0 до n.

    Args:
        n (int): Позиция числа Фибоначчи.

    Returns:
        int: n-е число Фибоначчи.

    Временная сложность: O(n)
    Пространственная сложность: O(n) — для массива dp.
    """
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def fib_optimized(n: int) -> int:
    """
    Возвращает n-е число Фибоначчи с оптимизацией по памяти.

    Использует только два переменных вместо массива.

    Args:
        n (int): Позиция числа Фибоначчи.

    Returns:
        int: n-е число Фибоначчи.

    Временная сложность: O(n)
    Пространственная сложность: O(1)
    """
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Решает задачу 0/1 рюкзака: максимизация стоимости при ограниченной вместимости.

    Каждый предмет можно взять не более одного раза.

    Args:
        weights (List[int]): Веса предметов.
        values (List[int]): Стоимости предметов.
        capacity (int): Максимальная грузоподъёмность.

    Returns:
        int: Максимальная достижимая стоимость.

    Временная сложность: O(n * W), где n — количество предметов, W — вместимость.
    Пространственная сложность: O(n * W)
    """
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        for c in range(1, capacity + 1):
            if w <= c:
                dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - w] + v)
            else:
                dp[i][c] = dp[i - 1][c]
    return dp[n][capacity]


def knapsack_01_with_items(
    weights: List[int], values: List[int], capacity: int
) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Возвращает максимальную стоимость и список выбранных предметов.

    Каждый предмет задаётся парой (стоимость, вес).

    Args:
        weights (List[int]): Веса предметов.
        values (List[int]): Стоимости предметов.
        capacity (int): Максимальная вместимость рюкзака.

    Returns:
        Tuple[int, List[Tuple[int, int]]]: Максимальная стоимость и список предметов.

    Временная сложность: O(n * W)
    Пространственная сложность: O(n * W)
    """
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        for c in range(1, capacity + 1):
            if w <= c:
                dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - w] + v)
            else:
                dp[i][c] = dp[i - 1][c]

    # Восстановление выбранных предметов
    items = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            items.append((values[i - 1], weights[i - 1]))
            c -= weights[i - 1]
    items.reverse()
    return dp[n][capacity], items


def knapsack_1d_optimized(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Оптимизированное решение 0/1 рюкзака с использованием одномерного массива.

    Позволяет сэкономить память за счёт обратного обхода.

    Args:
        weights (List[int]): Веса предметов.
        values (List[int]): Стоимости предметов.
        capacity (int): Вместимость рюкзака.

    Returns:
        int: Максимальная стоимость.

    Временная сложность: O(n * W)
    Пространственная сложность: O(W)
    """
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def lcs_length(str1: str, str2: str) -> int:
    """
    Вычисляет длину наибольшей общей подпоследовательности (LCS) двух строк.

    Подпоследовательность — это строка, полученная удалением некоторых символов без изменения порядка.

    Args:
        str1 (str): Первая строка.
        str2 (str): Вторая строка.

    Returns:
        int: Длина LCS.

    Временная сложность: O(n * m)
    Пространственная сложность: O(n * m)
    """
    n, m = len(str1), len(str2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]


def lcs_with_sequence(str1: str, str2: str) -> Tuple[int, str]:
    """
    Возвращает длину и саму наибольшую общую подпоследовательность (LCS).

    Args:
        str1 (str): Первая строка.
        str2 (str): Вторая строка.

    Returns:
        Tuple[int, str]: Длина LCS и строка LCS.

    Временная сложность: O(n * m)
    Пространственная сложность: O(n * m)
    """
    n, m = len(str1), len(str2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Восстановление последовательности
    seq = []
    i, j = n, m
    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            seq.append(str1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[n][m], "".join(reversed(seq))


def levenshtein_distance(str1: str, str2: str) -> int:
    """
    Вычисляет расстояние Левенштейна — минимальное число операций
    (вставка, удаление, замена), чтобы преобразовать str1 в str2.

    Args:
        str1 (str): Исходная строка.
        str2 (str): Целевая строка.

    Returns:
        int: Расстояние Левенштейна.

    Временная сложность: O(n * m)
    Пространственная сложность: O(n * m)
    """
    n, m = len(str1), len(str2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # удаление
                dp[i][j - 1] + 1,  # вставка
                dp[i - 1][j - 1] + cost,  # замена
            )
    return dp[n][m]


def fib_tabulation_with_trace(n: int) -> int:
    """
    Вычисляет n-е число Фибоначчи и выводит таблицу dp на каждом шаге.

    Используется для отладки и обучения.

    Args:
        n (int): Позиция числа Фибоначчи.

    Returns:
        int: n-е число Фибоначчи.

    Печатает:
        Таблицу индексов и значений F(i) после каждого шага.
    """
    if n <= 1:
        print(f"F({n}) = {n}")
        return n

    dp = [0] * (n + 1)
    dp[1] = 1
    print_fib_table(dp)

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        print_fib_table(dp)
    return dp[n]


def print_fib_table(dp: List[int]) -> None:
    """
    Печатает текущее состояние таблицы Фибоначчи в табличном виде.

    Args:
        dp (List[int]): Массив значений F(i).
    """
    print("i:  ", "  ".join(f"{i:2}" for i in range(len(dp))))
    print("F(i):", "  ".join(f"{val:2}" for val in dp))
    print()
