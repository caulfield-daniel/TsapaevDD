import kotlin.time.measureTime
import java.util.*

/**
 * Класс, хранящий результаты измерения производительности операций.
 * @property operation название операции (например, "Вставка в начало")
 * @property dataStructure тип структуры данных (например, "MutableList")
 * @property elements количество обработанных элементов
 * @property timeNs время выполнения операции в наносекундах
 */
data class PerformanceResult(
    val operation: String,
    val dataStructure: String,
    val elements: Int,
    val timeNs: Double
)

/**
 * Выполняет измерение времени выполнения различных операций над коллекциями.
 * @return список результатов с временем выполнения для каждой операции и структуры данных
 */
fun measurePerformance(): List<PerformanceResult> {
    val results = mutableListOf<PerformanceResult>()
    val testSizes = listOf(1000, 5000, 10000, 20000, 50000)

    for (size in testSizes) {
        // Тест вставки в начало
        val listInsertTime = measureTime {
            val list = mutableListOf<Int>()
            repeat(size) { list.add(0, it) }
        }.inWholeNanoseconds.toDouble()

        val linkedListInsertTime = measureTime {
            val ll = LinkedList<Int>()
            repeat(size) { ll.insertAtStart(it) }
        }.inWholeNanoseconds.toDouble()

        results.add(PerformanceResult("Вставка в начало", "MutableList", size, listInsertTime))
        results.add(PerformanceResult("Вставка в начало", "LinkedList", size, linkedListInsertTime))

        // Тест удаления из начала
        val listRemoveTime = measureTime {
            val list = MutableList(size) { it }
            repeat(size) { list.removeAt(0) }
        }.inWholeNanoseconds.toDouble()

        val dequeRemoveTime = measureTime {
            val deque = ArrayDeque<Int>().apply { repeat(size) { add(it) } }
            repeat(size) { deque.pollFirst() }
        }.inWholeNanoseconds.toDouble()

        results.add(PerformanceResult("Удаление из начала", "MutableList", size, listRemoveTime))
        results.add(PerformanceResult("Удаление из начала", "ArrayDeque", size, dequeRemoveTime))
    }

    return results
}