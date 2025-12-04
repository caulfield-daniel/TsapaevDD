from modules.greedy_algorithms import interval_scheduling
from modules.greedy_algorithms import fractional_knapsack
from modules.greedy_algorithms import (
    huffman_coding,
    generate_frequencies,
    build_tree,
    print_tree,
)
from modules.analysis import analysis
from modules.task import min_coins_greedy, prim_mst
from modules.performance_analysis import visualization

# === 1. Задача интервального планирования ===
print("1. ЗАДАЧА ИНТЕРВАЛЬНОГО ПЛАНИРОВАНИЯ")
print("-" * 40)
# Фиксированные интервалы для воспроизводимости
intervals = [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9)]
result = interval_scheduling(intervals)
print(f"Все интервалы: {intervals}")
print(f"Оптимальный выбор: {result}")
print(f"Количество выбранных интервалов: {len(result)}\n")

# === 2. Дробный рюкзак ===
print("2. ДРОБНЫЙ РЮКЗАК")
print("-" * 40)
# Явно заданные предметы: (стоимость, вес)
items = [(20, 4), (18, 3), (14, 2), (10, 1), (30, 5)]
capacity = 10
max_value = fractional_knapsack(items, capacity)
print(f"Предметы (стоимость, вес): {items}")
print(f"Ёмкость рюкзака: {capacity}")
print(f"Макс. стоимость (дробный): {max_value:.2f}\n")

# === 3. Кодирование Хаффмана ===
print("3. КОДИРОВАНИЕ ХАФФМАНА")
print("-" * 40)
# Текст с явным преобладанием некоторых символов
text = "aabbcccaaaaabbbccdddeeeeeaaaa"
freq = generate_frequencies(text)  # Теперь используем наш текст
codes = huffman_coding(freq)
print(f"Текст: '{text}'")
print(f"Частоты: {freq}")
print("Коды Хаффмана:")
for char, code in sorted(codes.items()):
    print(f"  '{char}': {code}")

tree = build_tree(codes)
print("\nДерево Хаффмана:")
print_tree(tree)
print()

# === 4. Сравнение алгоритмов рюкзака ===
print("4. СРАВНЕНИЕ АЛГОРИТМОВ РЮКЗАКА (0-1)")
print("-" * 40)
analysis()
print()

# === 5. Задача о монетах ===
print("5. ЗАДАЧА О МИНИМАЛЬНОМ КОЛИЧЕСТВЕ МОНЕТ")
print("-" * 40)
coins = [1, 5, 10, 25]  # Американские монеты
amount = 98
change = min_coins_greedy(coins, amount)
print(f"Монеты: {coins}")
print(f"Сумма: {amount}")
print(f"Сдача: {change}")
print(f"Количество монет: {len(change)}")
print(f"Разбиение: {dict((coin, change.count(coin)) for coin in set(change))}\n")

# === 6. Алгоритм Прима (MST) ===
print("6. АЛГОРИТМ ПРИМА — ПОИСК ОСТОВНОГО ДЕРЕВА")
print("-" * 40)
graph = [
    [0, 4, 0, 0, 0, 0, 0, 8, 0],
    [4, 0, 8, 0, 0, 0, 0, 11, 0],
    [0, 8, 0, 7, 0, 4, 0, 0, 2],
    [0, 0, 7, 0, 9, 14, 0, 0, 0],
    [0, 0, 0, 9, 0, 10, 0, 0, 0],
    [0, 0, 4, 14, 10, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 1, 6],
    [8, 11, 0, 0, 0, 0, 1, 0, 7],
    [0, 0, 2, 0, 0, 0, 6, 7, 0],
]
mst_edges, total_weight = prim_mst(graph)
print("Ребра остовного дерева:")
for u, v, w in mst_edges:
    print(f"  {u} -- {v} (вес: {w})")
print(f"Суммарный вес MST: {total_weight}\n")

# === 7. Визуализация производительности ===
print("7. ВИЗУАЛИЗАЦИЯ ПРОИЗВОДИТЕЛЬНОСТИ КОДА ХАФФМАНА")
print("-" * 40)
test_sizes = [500, 1000, 2000, 5000, 10000]
print(f"Запуск визуализации для размеров: {test_sizes}")
visualization(test_sizes)

# === Информация о системе ===
pc_info = """
    8. Характеристики ПК для тестирования:
    - Процессор: AMD Ryzen 7 5800H 3.20GHz
    - Оперативная память: 16 GB DDR4
    - ОС: Windows 11
    - Python: 3.12.10
    """
print(pc_info)
