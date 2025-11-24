"""
Практические задачи с применением рекурсии
"""

import os


def binary_search(arr, target, low=0, high=None):
    """
    Рекурсивная реализация бинарного поиска

    Args:
        arr (list): Отсортированный массив
        target: Искомый элемент
        low (int): Нижняя граница поиска
        high (int): Верхняя граница поиска

    Returns:
        int: Индекс элемента или -1 если не найден

    Time Complexity: O(log n)
    Recursion Depth: O(log n)
    """
    if high is None:
        high = len(arr) - 1

    # Базовый случай - элемент не найден
    if low > high:
        return -1

    mid = (low + high) // 2

    # Базовый случай - элемент найден
    if arr[mid] == target:
        return mid

    # Рекурсивный шаг - поиск в левой или правой половине
    elif arr[mid] > target:
        return binary_search(arr, target, low, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, high)


def recursive_file_system_tree(start_path, indent="", max_depth=None, current_depth=0):
    """
    Рекурсивный обход файловой системы

    Args:
        start_path (str): Начальный путь для обхода
        indent (str): Отступ для визуализации иерархии
        max_depth (int): Максимальная глубина рекурсии
        current_depth (int): Текущая глубина рекурсии

    Returns:
        list: Список всех найденных файлов и директорий
    """
    if max_depth is not None and current_depth > max_depth:
        return []

    try:
        items = os.listdir(start_path)
    except PermissionError:
        print(f"{indent}[Доступ запрещен] {os.path.basename(start_path)}/")
        return []
    except FileNotFoundError:
        print(f"{indent}[Путь не найден] {start_path}")
        return []

    items.sort()  # Сортировка для единообразного вывода
    result = []

    for i, item in enumerate(items):
        item_path = os.path.join(start_path, item)
        is_last = i == len(items) - 1

        if os.path.isdir(item_path):
            # Директория - рекурсивный обход
            prefix = "└── " if is_last else "├── "
            print(f"{indent}{prefix}{item}/")
            result.append(item_path + "/")

            new_indent = indent + ("    " if is_last else "│   ")
            sub_items = recursive_file_system_tree(
                item_path, new_indent, max_depth, current_depth + 1
            )
            result.extend(sub_items)
        else:
            # Файл
            prefix = "└── " if is_last else "├── "
            print(f"{indent}{prefix}{item}")
            result.append(item_path)

    return result


def hanoi_towers(n, source="A", target="C", auxiliary="B", moves=None):
    """
    Решение задачи о Ханойских башнях

    Args:
        n (int): Количество дисков
        source (str): Стержень-источник
        target (str): Стержень-назначение
        auxiliary (str): Вспомогательный стержень
        moves (list): Список для сохранения ходов

    Returns:
        list: Список ходов для решения задачи

    Time Complexity: O(2^n)
    Recursion Depth: O(n)
    """
    if moves is None:
        moves = []

    # Базовый случай - перемещение одного диска
    if n == 1:
        move = f"Переместить диск 1 со стержня {source} на стержень {target}"
        moves.append(move)
        print(move)
        return moves

    # Рекурсивный шаг:
    # 1. Переместить n-1 дисков на вспомогательный стержень
    hanoi_towers(n - 1, source, auxiliary, target, moves)

    # 2. Переместить самый большой диск на целевой стержень
    move = f"Переместить диск {n} со стержня {source} на стержень {target}"
    moves.append(move)
    print(move)

    # 3. Переместить n-1 дисков с вспомогательного на целевой стержень
    hanoi_towers(n - 1, auxiliary, target, source, moves)

    return moves


def calculate_hanoi_moves(n):
    """
    Вычисление минимального количества ходов для Ханойских башень

    Args:
        n (int): Количество дисков

    Returns:
        int: Минимальное количество ходов
    """
    if n == 1:
        return 1
    return 2 * calculate_hanoi_moves(n - 1) + 1


# Экспериментальное исследование
def experimental_analysis():
    """Проведение экспериментального исследования"""
    print("\n=== Экспериментальное исследование ===")

    # Измерение максимальной глубины рекурсии для файловой системы
    test_dir = "."  # Текущая директория
    print(f"Обход файловой системы для: {os.path.abspath(test_dir)}")
    all_items = recursive_file_system_tree(test_dir, max_depth=3)
    print(f"Найдено элементов: {len(all_items)}")

    # Анализ Ханойских башень
    print(f"\nХанойские башни для 3 дисков:")
    moves = hanoi_towers(3)
    print(f"Общее количество ходов: {len(moves)}")
    print(f"Теоретическое количество ходов: {calculate_hanoi_moves(3)}")


if __name__ == "__main__":
    # Тест бинарного поиска
    print("=== Бинарный поиск ===")
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 11
    index = binary_search(sorted_array, target)
    print(f"Массив: {sorted_array}")
    print(f"Элемент {target} найден по индексу: {index}")

    experimental_analysis()
