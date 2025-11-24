"""
Классические рекурсивные алгоритмы
"""

def factorial(n):
    """
    Вычисление факториала числа n рекурсивным методом
    
    Args:
        n (int): Неотрицательное целое число
    
    Returns:
        int: Факториал числа n
    
    Time Complexity: O(n)
    Recursion Depth: O(n)
    """
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    if n == 0 or n == 1:  # Базовый случай
        return 1
    return n * factorial(n - 1)  # Рекурсивный шаг


def fibonacci(n):
    """
    Вычисление n-го числа Фибоначчи наивным рекурсивным методом
    
    Args:
        n (int): Порядковый номер числа Фибоначчи
    
    Returns:
        int: n-е число Фибоначчи
    
    Time Complexity: O(2^n)
    Recursion Depth: O(n)
    """
    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    if n == 0:  # Базовый случай
        return 0
    if n == 1:  # Базовый случай
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)  # Рекурсивный шаг


def fast_power(a, n):
    """
    Быстрое возведение числа a в степень n через степень двойки
    
    Args:
        a (float/int): Основание
        n (int): Показатель степени (неотрицательный)
    
    Returns:
        float/int: a в степени n
    
    Time Complexity: O(log n)
    Recursion Depth: O(log n)
    """
    if n < 0:
        raise ValueError("Показатель степени должен быть неотрицательным")
    if n == 0:  # Базовый случай
        return 1
    if n == 1:  # Базовый случай
        return a
    
    half_power = fast_power(a, n // 2)  # Рекурсивный шаг
    
    if n % 2 == 0:
        return half_power * half_power
    else:
        return a * half_power * half_power


if __name__ == "__main__":
    print("=== Тестирование рекурсивных функций ===")
    

    print(f"Факториал 5: {factorial(5)}")  # 120
    print(f"Факториал 0: {factorial(0)}")  # 1
    
    print(f"Фибоначчи(6): {fibonacci(6)}")  # 8
    print(f"Фибоначчи(10): {fibonacci(10)}")  # 55
    
    print(f"2^10: {fast_power(2, 10)}")  # 1024
    print(f"3^5: {fast_power(3, 5)}")    # 243