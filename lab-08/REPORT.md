# Отчет по лабораторной работе 8. Жадные алгоритмы

**Дата:** 2025-04-12

**Семестр:** 3 курс 5 семестр

**Группа:** ПИЖ-б-о-23-2(1)

**Дисциплина:** Анализ сложности алгоритмов

**Студент:** Цапаев Данил Денисович

## Цель работы

Изучить метод проектирования алгоритмов, известный как "жадный алгоритм". Освоить принцип принятия локально оптимальных решений на каждом шаге и понять условия, при которых этот подход приводит к глобально оптимальному решению. Получить практические навыки реализации жадных алгоритмов для решения классических задач, анализа их корректности и оценки эффективности.

## Практическая часть

### Выполненные задачи

- [ ] Реализовать классические жадные алгоритмы.
- [ ] Проанализировать их корректность (доказать или объяснить, почему жадный выбор приводит к оптимальному решению).
- [ ] Провести сравнительный анализ эффективности жадного подхода и других методов (например, полного перебора для маленьких входных данных).
- [ ] Решить практические задачи с применением жадного подхода.

### Ключевые фрагменты кода

```PYTHON
# greedy_algorithms.py

import heapq
import random
import string
from typing import List, Tuple, Dict, Union


def generate_intervals(
    n: int, start_range: int = 0, end_range: int = 1000
) -> List[Tuple[int, int]]:
    """
    Генерирует список случайных непустых интервалов [start, end).

    Args:
        n: количество интервалов
        start_range: минимальное значение начала интервала
        end_range: максимальное значение конца интервала

    Returns:
        Список кортежей вида (start, end)
    """
    intervals = []
    for _ in range(n):
        start = random.randint(start_range, end_range - 1)
        end = random.randint(start + 1, end_range)
        intervals.append((start, end))
    return intervals


def interval_scheduling(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Жадный алгоритм для задачи выбора максимального количества непересекающихся интервалов.

    Args:
        intervals: список интервалов (start, end)

    Returns:
        Список выбранных непересекающихся интервалов
    """
    # Сортируем по времени окончания — ключевая идея алгоритма
    intervals.sort(key=lambda x: x[1])

    selected = []
    last_end = float("-inf")

    for start, end in intervals:
        if start >= last_end:
            selected.append((start, end))
            last_end = end

    return selected


def generate_items(
    n: int,
    value_range: Tuple[int, int] = (10, 100),
    weight_range: Tuple[int, int] = (1, 50),
) -> List[Tuple[int, int]]:
    """
    Генерирует список случайных предметов для задачи о рюкзаке.

    Args:
        n: количество предметов
        value_range: диапазон значений (min, max)
        weight_range: диапазон весов (min, max)

    Returns:
        Список кортежей (value, weight)
    """
    return [
        (random.randint(*value_range), random.randint(*weight_range)) for _ in range(n)
    ]


def fractional_knapsack(items: List[Tuple[int, int]], capacity: int) -> float:
    """
    Решает задачу о дробном рюкзаке с помощью жадного алгоритма.

    Args:
        items: список (value, weight)
        capacity: максимальная грузоподъёмность

    Returns:
        Максимальная суммарная стоимость
    """
    # Сортируем по убыванию удельной стоимости
    items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)

    total_value = 0.0
    remaining_capacity = capacity

    for value, weight in items:
        if remaining_capacity == 0:
            break
        if weight <= remaining_capacity:
            total_value += value
            remaining_capacity -= weight
        else:
            fraction = remaining_capacity / weight
            total_value += value * fraction
            break  # после этого рюкзак заполнен

    return total_value


def generate_text(length: int) -> str:
    """
    Генерирует случайную строку из заглавных латинских букв.

    Args:
        length: длина строки

    Returns:
        Случайная строка
    """
    return "".join(random.choices(string.ascii_uppercase, k=length))


def generate_frequencies(text: str) -> Dict[str, int]:
    """
    Подсчитывает частоту символов в строке.

    Args:
        text: входная строка

    Returns:
        Словарь {символ: частота}
    """
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    return freq


class Node:
    """Узел для построения дерева Хаффмана."""

    __slots__ = ("char", "freq", "left", "right")

    def __init__(self, char: Union[str, None], freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other: "Node") -> bool:
        return self.freq < other.freq


def huffman_coding(frequencies: Dict[str, int]) -> Dict[str, str]:
    """
    Строит коды Хаффмана для заданных частот символов.

    Args:
        frequencies: словарь {символ: частота}

    Returns:
        Словарь {символ: двоичный код}
    """
    if not frequencies:
        return {}

    # Создаем мин-кучу из узлов
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    # Строим дерево: объединяем два узла с наименьшей частотой
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    root = heap[0]
    codes = {}

    def _generate_codes(node: Node, code: str):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = code
            return
        _generate_codes(node.left, code + "0")
        _generate_codes(node.right, code + "1")

    _generate_codes(root, "")
    return codes


def build_tree(codes: Dict[str, str]) -> Dict:
    """
    Строит словарное дерево для визуализации префиксных кодов.

    Args:
        codes: словарь {символ: код}

    Returns:
        Вложенный словарь, представляющий бинарное дерево
    """
    tree = {}
    for char, code in codes.items():
        node = tree
        for bit in code:
            node = node.setdefault(bit, {})
        node["char"] = char
    return tree


def print_tree(node: Dict, prefix: str = "") -> None:
    """
    Рекурсивно выводит структуру дерева в читаемом виде.

    Args:
        node: текущий узел дерева
        prefix: префикс для отступов
    """
    for key in sorted(node.keys()):
        if key == "char":
            print(f"{prefix}: {node[key]}")
        else:
            print(f"{prefix}{key}")
            print_tree(node[key], prefix + "  ")

```

```PYTHON
# analysis.py
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

```

```PYTHON
# task.py

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

```

```PYTHON
import matplotlib.pyplot as plt
import timeit
from typing import List
from modules.greedy_algorithms import (
    huffman_coding,
    generate_frequencies,
    generate_text,
)


def measure_huffman_time(size: int, repeats: int = 3) -> float:
    """
    Измеряет время выполнения алгоритма Хаффмана для текста заданного размера.

    Args:
        size: размер текста (количество символов)
        repeats: количество повторов для усреднения

    Returns:
        среднее время выполнения в миллисекундах
    """

    def execution_time() -> None:
        text = generate_text(size)
        frequencies = generate_frequencies(text)
        huffman_coding(frequencies)

    total_time = timeit.timeit(execution_time, number=repeats)
    return (total_time / repeats) * 1000  # в миллисекундах


def visualization(sizes: List[int]) -> None:
    """
    Визуализация времени выполнения алгоритма Хаффмана.

    Args:
        sizes: список размеров текста для тестирования
    """
    huffman_times: List[float] = [measure_huffman_time(size) for size in sizes]

    print("Время выполнения алгоритма Хаффмана для разных размеров:")
    print(huffman_times)
    print()

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, huffman_times, marker="o", color="red", label="Huffman")
    plt.xlabel("Количество элементов, n")
    plt.ylabel("Время выполнения, ms")
    plt.title("Время выполнения алгоритма Хаффмана")
    plt.legend(loc="upper left", title="Метод")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("./report/Huffman.png", dpi=300, bbox_inches="tight")
    plt.show()

```

```PYTHON
# main.py

from modules.greedy_algorithms import interval_scheduling, generate_intervals
from modules.greedy_algorithms import fractional_knapsack, generate_items
from modules.greedy_algorithms import (huffman_coding, generate_frequencies,
                                       generate_text, build_tree, print_tree)
from modules.analysis import analysis
from modules.task import min_coins_greedy, prim_mst
from modules.perfomance_analysis import visualization

# Пример использования:
intervals = generate_intervals(50)
result = interval_scheduling(intervals)
print("Выбранные интервалы:", result)

print("\n")

# Пример использования:
items = generate_items(10)
capacity = 50

result = fractional_knapsack(items, capacity)
print(f"Максимальная стоимость: {result:.2f}")

print("\n")

# Пример использования:
frequencies = generate_frequencies(generate_text(50))

codes = huffman_coding(frequencies)
print("Коды Хаффмана:")
for char, code in codes.items():
    print(f"{char}: {code}")

tree = build_tree(codes)
print_tree(tree)

print("\n")

# Запуск анализа и сравнения алгоритмов рюкзака
analysis()

print("\n")

# Пример: стандартная система монет (рубли)
coins = [1, 2, 5, 10]
amount = 28

result = min_coins_greedy(coins, amount)
print("Сдача:", result)
print("Количество монет:", len(result))

print("\n")

# Пример графа (матрица смежности)
graph = [
    [0, 2, 0, 6, 0],
    [2, 0, 3, 8, 5],
    [0, 3, 0, 0, 7],
    [6, 8, 0, 0, 9],
    [0, 5, 7, 9, 0]
]

mst_edges, total_weight = prim_mst(graph)
print("Ребра MST:")
for u, v, w in mst_edges:
    print(f"{u} - {v} (вес {w})")
print("Суммарный вес MST:", total_weight)

print("\n")

# Визуализация времени выполнения алгоритма Хаффмана
sizes = [1000, 5000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
visualization(sizes)

```

![]

```bash
Выбранные интервалы: [(119, 135), (265, 292), (404, 441), (611, 614), (632, 633), (647, 654), (791, 847), (877, 892), (904, 932), (956, 960)]


Максимальная стоимость: 223.04


Коды Хаффмана:
M: 000
U: 001
K: 010
Z: 0110
Y: 0111
N: 1000
C: 1001
X: 101000
P: 101001
G: 10101
D: 1011
R: 110000
H: 110001
W: 110010
J: 110011
E: 1101
I: 11100
O: 11101
T: 111100
Q: 111101
V: 11111
0
  0
    0
      : M
    1
      : U
  1
    0
      : K
    1
      0
        : Z
      1
        : Y
1
  0
    0
      0
        : N
      1
        : C
    1
      0
        0
          0
            : X
          1
            : P
        1
          : G
      1
        : D
  1
    0
      0
        0
          0
            : R
          1
            : H
        1
          0
            : W
          1
            : J
      1
        : E
    1
      0
        0
          : I
        1
          : O
      1
        0
          0
            : T
          1
            : Q
        1
          : V


Рюкзак емкостью: 50
Предметы (стоимость, вес): [(60, 10), (100, 20), (120, 30)]
Жадный алгоритм (непрерывный рюкзак): 240.0
Жадный алгоритм (дискретный 0-1 рюкзак): 160 [(60, 10), (100, 20)]
Точный перебор (дискретный 0-1 рюкзак): 220 ((100, 20), (120, 30))


Сдача: [10, 10, 5, 2, 1]
Количество монет: 5


Ребра MST:
0 - 1 (вес 2)
1 - 2 (вес 3)
0 - 3 (вес 6)
1 - 4 (вес 5)
Суммарный вес MST: 16


Время выполнения алгоритма Хаффмана для разных размеров:
[0.03256666241213679, 0.032966655756657325, 0.03390000589812795, 0.04913331940770149, 0.043100008042529225, 0.048199998370061316, 0.04673333023674786]

Характеристики ПК для тестирования:
    - Процессор: AMD Ryzen 7 5800H 3.20GHz
    - Оперативная память: 16 GB DDR4
    - ОС: Windows 11
    - Python: 3.12.10
```

## **Для каждого алгоритма указать его временную сложность и объяснить, почему жадный выбор корректен**

| Алгоритм | Временная сложность | Обоснование корректности жадного выбора |
|-----------|----------------------|------------------------------------------|
| **Алгоритм Хаффмана (Huffman Coding)** | `O(n log n)` | На каждом шаге объединяются два узла с наименьшими частотами. Это минимизирует рост общей длины кодов. Любое другое объединение привело бы к большей суммарной длине. Жадный выбор корректен. |
| **Непрерывный рюкзак (Fractional Knapsack)** | `O(n log n)` | Предметы сортируются по убыванию удельной стоимости (ценность/вес). Так как можно брать дробные части, локальный выбор предмета с максимальной удельной ценностью всегда ведёт к глобальному максимуму стоимости. |
| **Задача о выборе заявок (Interval Scheduling)** | `O(n log n)` | Интервалы сортируются по времени окончания, и выбирается первый непересекающийся. Замена любого интервала, начинающегося позже, на более ранний по окончанию не уменьшает количество выбранных интервалов. Поэтому жадный выбор — оптимален. |

## **Анализ корректности:**

### Алгоритм Хаффмана (Huffman Coding)

Жадная стратегия заключается в объединении двух символов с наименьшими частотами на каждом шаге.  
Это минимизирует увеличение общей длины кодов, потому что редко встречающиеся символы получают более длинные коды, не влияя на частые символы.  
Такой выбор локально оптимален на каждом этапе и приводит к глобально оптимальному префиксному коду.

---

### Непрерывный рюкзак (Fractional Knapsack)

Жадная стратегия состоит в том, чтобы сначала брать предметы с наибольшей удельной стоимостью (ценность/вес).  
Поскольку можно брать дробные части предметов, такой выбор всегда обеспечивает максимальный прирост стоимости на единицу веса.  
Следовательно, последовательное добавление наиболее «выгодных» предметов приводит к оптимальному результату.

---

### Задача о выборе заявок (Interval Scheduling)

Жадная стратегия — выбирать интервалы, которые заканчиваются раньше всех и не пересекаются с уже выбранными.  
Это позволяет освободить как можно больше времени для последующих заявок.  
Так как любой другой выбор не увеличит число совместимых интервалов, жадная стратегия приводит к оптимальному решению.

## Сравнение эффективности жадных алгоритмов с наивными реализациями

| Алгоритм | Жадный подход | Наивная/переборная реализация | Временная сложность | Комментарий |
|-----------|---------------|-------------------------------|-------------------|-------------|
| **Задача о выборе заявок (Interval Scheduling)** | Сортировка по времени окончания + выбор непересекающихся интервалов | Перебор всех подмножеств интервалов | O(n log n) | Жадный алгоритм всегда даёт оптимальное решение. Перебор — O(2^n), сильно медленнее при больших n. |
| **Непрерывный рюкзак (Fractional Knapsack)** | Сортировка по удельной стоимости + добавление максимально возможного предмета | Перебор всех комбинаций предметов | O(n log n) | Жадный подход оптимален только для дробного рюкзака. Перебор для дискретного рюкзака (0-1) имеет сложность O(2^n). |
| **Алгоритм Хаффмана** | Построение минимальной кучи, объединение двух узлов с минимальной частотой | Перебор всех возможных деревьев (непрактично) | O(n log n) | Жадный выбор минимальных частот гарантирует оптимальный префиксный код. Полный перебор для больших n невозможен. |
| **Задача сдачи монет (стандартная система)** | Всегда брать максимальную доступную монету | Перебор всех комбинаций монет для минимизации их числа | O(n) | Работает корректно только для канонических систем монет. Перебор всегда даёт оптимальное решение, но сильно медленнее. |
| **Минимальное остовное дерево (Prim)** | На каждом шаге добавляем минимальное ребро, соединяющее MST с остальными вершинами | Проверка всех возможных подмножеств ребер | O(V^2) или O(E log V) с кучей | Жадный подход всегда даёт MST. Перебор всех подмножеств ребер имеет экспоненциальную сложность. |

---

## Ограничения жадного подхода

| Ограничение | Пояснение | Пример |
|-------------|-----------|--------|
| Локальная оптимальность не всегда ведёт к глобальной | Жадный выбор делает оптимальное локальное решение, но это не гарантирует глобальное | Дискретный рюкзак 0-1: жадный алгоритм по удельной стоимости может пропустить оптимальную комбинацию предметов |
| Требуется каноническая или «правильная» структура данных | Для корректной работы жадного алгоритма нужна определённая система весов/монет | Сдача монет: для системы [1, 3, 4] жадный подход может не дать минимальное количество монет |
| Не применим для всех задач оптимизации | Некоторые задачи требуют глобального анализа или динамического программирования | Задача коммивояжёра, где жадный выбор ближайшего города не гарантирует минимальный путь |
| Чувствителен к сортировке/критерию выбора | Ошибочный критерий может привести к неоптимальному решению | Рюкзак: если сортировать предметы не по удельной стоимости, а по весу, результат не будет оптимальным |

## Ответы на контрольные вопросы

### 1. Основная идея жадных алгоритмов

Жадный алгоритм принимает решения **шаг за шагом**, на каждом шаге выбирая **локально оптимальный вариант**, который кажется наилучшим в данный момент.  
Цель состоит в том, чтобы комбинация этих локальных оптимумов привела к **глобально оптимальному решению**.  
Жадные алгоритмы эффективны, когда локальный оптимум гарантирует глобальный.

---

### 2. Жадный алгоритм для задачи о выборе заявок (Interval Scheduling)

Жадная стратегия выбирает **интервалы с наименьшим временем окончания**, которые не пересекаются с уже выбранными.  
Почему это работает:  

- Выбирая рано заканчивающийся интервал, мы оставляем **максимально возможное пространство для последующих интервалов**.  
- Любой другой выбор, начинающийся позже, либо пересекается с текущим, либо оставляет меньше места для будущих интервалов.  
Таким образом, локальный оптимум (раннее окончание) гарантирует **максимальное количество непересекающихся интервалов**.

---

### 3. Примеры задач с оптимальным и не оптимальным применением жадного алгоритма

| Задача | Жадный алгоритм дает оптимальное решение? | Комментарий |
|--------|-----------------------------------------|-------------|
| Interval Scheduling (выбор заявок) |  Да | Выбор по раннему окончанию всегда оптимален |
| Fractional Knapsack (непрерывный рюкзак) |  Да | Можно брать дробные части предметов |
| 0-1 Knapsack (дискретный рюкзак) |  Нет | Жадный выбор по удельной стоимости может пропустить оптимальную комбинацию предметов |
| Coin Change для нестандартных монет [1,3,4] |  Нет | Жадный выбор наибольшей монеты не всегда минимизирует количество монет |

---

### 4. Разница между непрерывной (дробной) и дискретной (0-1) задачами о рюкзаке

- **Непрерывный рюкзак (Fractional Knapsack):** можно брать **любую часть предмета**, пропорционально его весу.  
  - Жадный алгоритм по удельной стоимости (value/weight) **всегда оптимален**.  

- **Дискретный рюкзак (0-1 Knapsack):** каждый предмет можно взять **либо целиком, либо не брать**.  
  - Жадный подход **не гарантирует оптимального решения**, нужно использовать динамическое программирование или перебор.  

| Характеристика | Непрерывный рюкзак | Дискретный рюкзак |
|----------------|------------------|-----------------|
| Возможность дробления предметов |  Да |  Нет |
| Оптимальность жадного алгоритма |  Да |  Нет |
| Сложность точного решения | O(n log n) | O(2^n) перебор / O(nW) динамика |
| Используемый критерий | Удельная стоимость (value/weight) | Обычно динамика или перебор |

---

### 5. Жадный алгоритм построения кода Хаффмана и его оптимальность

**Алгоритм Хаффмана:**

1. Для каждого символа создаём узел с его частотой.  
2. Формируем **минимальную кучу** по частотам.  
3. Пока в куче больше одного узла:  
   - Извлекаем два узла с наименьшими частотами.  
   - Создаём новый узел с суммарной частотой и присоединяем два узла как дочерние.  
   - Добавляем новый узел обратно в кучу.  
4. После окончания остаётся одно дерево, из которого строим коды: левый путь = `0`, правый путь = `1`.

**Оптимальность:**

- На каждом шаге объединяются **символы с минимальными частотами**, что минимизирует суммарную длину кодов.  
- Жадный выбор минимальных частот гарантирует **минимальную среднюю длину префиксного кода**, что и требуется для эффективной компрессии.
