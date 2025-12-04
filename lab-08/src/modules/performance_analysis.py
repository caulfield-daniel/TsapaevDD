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
    plt.savefig("huffman.png", dpi=300, bbox_inches="tight")
    plt.show()
