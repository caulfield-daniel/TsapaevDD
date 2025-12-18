import sys
from modules.comparison import run_analysis
from modules.dynamic_programming import (
    lcs_with_sequence,
    fib_tabulation_with_trace
)
from modules.tasks import coin_change, lis
from modules.perfomance_analysis import (
    visualization_knapsack,
    visualization_fib,
    visualization_lcs,
    visualization_levenshtein
)


# Увеличиваем лимит рекурсии для работы с большими значениями
sys.setrecursionlimit(30000)


def main() -> None:
    """
    Основная функция запуска лабораторной работы.
    Выполняет:
    - Сравнение алгоритмов Фибоначчи (мемоизация vs табуляция)
    - Сравнение жадного алгоритма и ДП для рюкзака
    - Демонстрацию работы LCS, размена монет и LIS
    - Анализ производительности различных алгоритмов ДП
    - Вывод характеристик системы
    """
    print("=== Сравнение алгоритмов динамического программирования ===\n")

    # --- Сравнение алгоритмов Фибоначчи и рюкзака ---
    run_analysis()

    print("\n" + "="*60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ АЛГОРИТМОВ")
    print("="*60)

    # Пример LCS
    length, subseq = lcs_with_sequence("AGGTAB", "GXTXAYB")
    print(f"LCS: Длина = {length}, Подпоследовательность = '{subseq}'")

    # Пример размена монет
    coins = [1, 2, 5]
    amount = 11
    min_coins = coin_change(coins, amount)
    print(f"Минимальное количество монет для суммы {amount}: {min_coins}")

    # Пример LIS
    seq = [10, 22, 9, 33, 21, 50, 41, 60]
    length, subsequence = lis(seq)
    print(f"Длина LIS: {length}")
    print(f"LIS: {subsequence}")

    print("\n" + "="*60)
    print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ АЛГОРИТМОВ")
    print("="*60)

    # Визуализация производительности
    n_values_fib = [100, 1000, 5000, 10000, 25000]
    print("Анализ производительности: Числа Фибоначчи...")
    visualization_fib(n_values_fib)

    capacities = list(range(100, 501, 100))
    print("Анализ производительности: Задача о рюкзаке...")
    visualization_knapsack(capacities)

    lengths = [10, 50, 100, 250, 500, 1000, 2500, 10000]
    print("Анализ производительности: LCS...")
    visualization_lcs(lengths)
    print("Анализ производительности: Расстояние Левенштейна...")
    visualization_levenshtein(lengths)

    # Демонстрация трассировки вычисления Фибоначчи
    print("\n" + "="*60)
    print("ТРАССИРОВКА ВЫЧИСЛЕНИЯ ЧИСЕЛ ФИБОНАЧЧИ")
    print("="*60)
    print("Построение таблицы значений F(i) для n = 10:\n")
    fib_tabulation_with_trace(10)

    # Информация о системе
    pc_info = """
Характеристики ПК для тестирования:
    - Процессор: AMD Ryzen 7 5800H 3.20GHz
    - Оперативная память: 16 GB DDR4
    - ОС: Windows 11
    - Python: 3.12.10
    """
    print(pc_info)


if __name__ == "__main__":
    main()
