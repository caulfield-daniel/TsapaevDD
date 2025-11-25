"""
Анализ производительности и визуализация результатов
"""

import time
import matplotlib.pyplot as plt
from recursion import fibonacci as naive_fibonacci
from memoization import fibonacci_memoized
import platform
import sys
from recursion import fast_power
from recursion import factorial


def measure_performance():
    """
    Замер времени выполнения для разных n
    """
    n_values = list(range(10, 36, 5))
    times_naive = []
    times_memoized = []

    print("=== Измерение производительности ===")
    print(f"{'n':<5} {'Наивная (с)':<12} {'Мемоизация (с)':<15}")
    print("-" * 40)

    for n in n_values:
        # Наивная реализация
        start_time = time.perf_counter()
        try:
            naive_result = naive_fibonacci(n)
            naive_time = time.perf_counter() - start_time
        except RecursionError:
            naive_time = float("inf")
            naive_result = "Error"

        # Для очень быстрых вычислений делаем несколько итераций
        if naive_time < 0.001:  # Если время очень мало
            iterations = 1000
            start_time = time.perf_counter()
            try:
                for _ in range(iterations):
                    naive_fibonacci(n)
                naive_time = (time.perf_counter() - start_time) / iterations
            except RecursionError:
                pass

        # Мемоизированная реализация
        start_time = time.perf_counter()
        memo_result = fibonacci_memoized(n)
        memo_time = time.perf_counter() - start_time

        # Для очень быстрых вычислений делаем несколько итераций
        if memo_time < 0.001:  # Если время очень мало
            iterations = 10000  # Больше итераций для очень быстрой функции
            start_time = time.perf_counter()
            for _ in range(iterations):
                fibonacci_memoized(n)
            memo_time = (time.perf_counter() - start_time) / iterations

        times_naive.append(naive_time if naive_time != float("inf") else None)
        times_memoized.append(memo_time)

        # Форматируем вывод для очень малых значений
        naive_str = (
            f"{naive_time:.6f}" if naive_time >= 0.000001 else f"{naive_time:.2e}"
        )
        memo_str = f"{memo_time:.6f}" if memo_time >= 0.000001 else f"{memo_time:.2e}"

        print(f"{n:<5} {naive_str:<12} {memo_str:<15}")

    return n_values, times_naive, times_memoized


def plot_comparison(n_values, times_naive, times_memoized):
    """
    Построение графика сравнения производительности
    """
    plt.figure(figsize=(12, 6))

    # Фильтруем значения, где наивная реализация не вызвала ошибку
    valid_indices = [i for i, t in enumerate(times_naive) if t is not None and t > 0]
    valid_n = [n_values[i] for i in valid_indices]
    valid_naive = [times_naive[i] for i in valid_indices]
    valid_memo = [times_memoized[i] for i in valid_indices]

    plt.plot(
        valid_n, valid_naive, "ro-", label="Наивная рекурсия", linewidth=2, markersize=6
    )
    plt.plot(
        n_values,
        times_memoized,
        "go-",
        label="С мемоизацией",
        linewidth=2,
        markersize=6,
    )

    plt.xlabel("n (номер числа Фибоначчи)")
    plt.ylabel("Время выполнения (секунды)")
    plt.title("Сравнение производительности: наивная рекурсия vs мемоизация")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("fibonacci_performance.png", dpi=300, bbox_inches="tight")
    plt.show()


def analyze_recursion_depth():
    """
    Анализ глубины рекурсии для разных алгоритмов
    """
    print("\n=== Анализ глубины рекурсии ===")

    original_limit = sys.getrecursionlimit()
    print(f"Текущий лимит рекурсии: {original_limit}")

    # Тестирование на разных значениях
    test_values = [5, 10, 20, 100, 500, 1000]

    print(f"{'n':<8} {'Факториал':<12} {'Быстрая степень':<18}")
    print("-" * 45)

    for n in test_values:
        try:
            # Факториал - глубина рекурсии O(n)
            factorial(n)
            fact_ok = "✓"
        except RecursionError:
            fact_ok = "✗"

        try:
            # Быстрая степень - глубина рекурсии O(log n)
            fast_power(2, n)
            power_ok = "✓"
        except RecursionError:
            power_ok = "✗"

        print(f"{n:<8} {fact_ok:<12} {power_ok:<18}")


if __name__ == "__main__":
    # Характеристики ПК

    print("=== Характеристики тестовой системы ===")
    print(f"ОС: {platform.system()} {platform.release()}")
    print(f"Процессор: {platform.processor()}")
    print(f"Память: 16.0 GB")
    print(f"Python: {platform.python_version()}")

    # Измерение производительности
    n_vals, naive_times, memo_times = measure_performance()

    # Построение графиков
    plot_comparison(n_vals, naive_times, memo_times)

    # Анализ глубины рекурсии
    analyze_recursion_depth()
