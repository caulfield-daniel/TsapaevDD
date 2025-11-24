"""
Оптимизация рекурсивных алгоритмов с помощью мемоизации
"""

import time
from functools import wraps
from recursion import fibonacci as naive_fibonacci


def memoize(func):
    """
    Декоратор для мемоизации функции
    """
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


@memoize
def fibonacci_memoized(n):
    """
    Вычисление n-го числа Фибоначчи с мемоизацией

    Args:
        n (int): Порядковый номер числа Фибоначчи

    Returns:
        int: n-е число Фибоначчи

    Time Complexity: O(n) с мемоизацией
    Recursion Depth: O(n)
    """
    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


# Версия с явным кешированием (альтернативная реализация)
def fibonacci_explicit_memo(n, cache=None):
    """
    Вычисление n-го числа Фибоначчи с явной мемоизацией

    Args:
        n (int): Порядковый номер числа Фибоначчи
        cache (dict): Кеш для мемоизации

    Returns:
        int: n-е число Фибоначчи
    """
    if cache is None:
        cache = {}

    if n in cache:
        return cache[n]

    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    if n == 0:
        return 0
    if n == 1:
        return 1

    result = fibonacci_explicit_memo(n - 1, cache) + fibonacci_explicit_memo(
        n - 2, cache
    )
    cache[n] = result
    return result


def compare_performance():
    """
    Сравнение производительности наивной и мемоизированной версий
    """
    test_values = [10, 20, 30, 35]

    print("=== Сравнение производительности ===")
    print(f"{'n':<8} {'Наивная (с)':<15} {'Мемоизация (с)':<15} {'Результат':<10}")
    print("-" * 50)

    for n in test_values:
        # Наивная версия
        start_time = time.time()
        try:
            result_naive = naive_fibonacci(n)
            time_naive = time.time() - start_time
        except RecursionError:
            result_naive = "RecursionError"
            time_naive = "N/A"

        # Мемоизированная версия
        start_time = time.time()
        result_memo = fibonacci_memoized(n)
        time_memo = time.time() - start_time

        print(f"{n:<8} {str(time_naive):<15} {time_memo:<15.6f} {result_memo:<10}")


# Дополнительная функция для подсчета вызовов
class CallCounter:
    """Класс для подсчета количества рекурсивных вызовов"""

    def __init__(self):
        self.count = 0

    def fibonacci_counted(self, n):
        """Фибоначчи с подсчетом вызовов"""
        self.count += 1
        if n <= 1:
            return n
        return self.fibonacci_counted(n - 1) + self.fibonacci_counted(n - 2)


if __name__ == "__main__":
    compare_performance()

    # Подсчет количества вызовов для n=35
    print("\n=== Подсчет количества рекурсивных вызовов для n=10 ===")
    counter = CallCounter()
    result = counter.fibonacci_counted(10)
    print(f"Количество вызовов для наивной реализации (n=10): {counter.count}")
    print(f"Результат: {result}")
