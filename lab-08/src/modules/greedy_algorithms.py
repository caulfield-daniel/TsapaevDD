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
