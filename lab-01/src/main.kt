import kotlin.random.Random
import kotlin.time.Duration
import kotlin.time.measureTime
import kotlin.math.*
import java.io.File
import java.io.FileWriter

/**
 * Линейный поиск элемента в массиве.
 * @param array Массив для поиска
 * @param target Искомый элемент
 * @return Индекс найденного элемента или -1 если элемент не найден
 *
 * Алгоритмическая сложность: O(n) в худшем случае
 */
fun linearSearch(array: Array<Int>, target: Int): Int {
    if (array.isNotEmpty()) {                               // O(1) - проверка условия
        for (i in array.indices) {                          // O(n) - цикл выполняется n раз
            if (array[i] == target) return i                // O(1) - проверка условия, сравнение и возврат значения
        }
    }
    return -1                                               // O(1) - возврат значения

    // O(1) + O(n) * O(1) + O(1) = O(n)
}

/**
 * Бинарный поиск элемента в ОТСОРТИРОВАННОМ массиве.
 * @param array ОТСОРТИРОВАННЫЙ массив для поиска
 * @param target Искомый элемент
 * @return Индекс найденного элемента или -1 если элемент не найден
 *
 * Алгоритмическая сложность: O(log n)
 */
fun binarySearch(array: Array<Int>, target: Int): Int {
    var left = 0                                            // O(1) - инициализация переменной
    var right: Int = array.lastIndex                        // O(1) - получение lastIndex + инициализация

    if (array.isNotEmpty()) {                               // O(1) - проверка условия
        while (left <= right) {                             // O(log n) - цикл выполняется log₂(n) раз
            val mid = left + (right - left) / 2             // O(1) - вычисление среднего индекса
            when {                                          // O(1) - оператор выбора
                target == array[mid] -> return mid          // O(1) - сравнение + возврат
                target > array[mid] -> left = mid + 1       // O(1) - сравнение + присваивание
                else -> right = mid - 1                     // O(1) - присваивание
            }
        }
    }
    return -1                                               // O(1) - возврат значения

    // O(1) + O(1) + O(1) + [O(log n) × (O(1) + O(1))] + O(1) = O(log n)
}

/**
 * Измеряет среднее время выполнения функции поиска для конкретного массива и цели.
 * @param times Количество повторений для усреднения
 * @param searchFunction Функция поиска, время которой измеряется
 * @param array Массив для поиска
 * @param target Целевой элемент для поиска
 * @return Средняя продолжительность выполнения функции за times выполнений
 */
fun measureAverageTime(
    times: Int,
    searchFunction: (Array<Int>, Int) -> Int,
    array: Array<Int>,
    target: Int
): Duration {
    repeat(1000) {
        searchFunction(array, target)
    }

    var totalTime: Duration = Duration.ZERO

    repeat(times) {
        totalTime += measureTime { searchFunction(array, target) }
    }

    return totalTime / times
}

/**
 * Генерирует отсортированный массив заданного размера
 * @param size Размер массива
 * @return Отсортированный массив случайных чисел
 */
fun generateSortedArray(size: Int): Array<Int> {
    return Array(size) { Random.nextInt(0, size * 10) }.sortedArray()
}

/**
 * Тестирует алгоритмы поиска на массивах разного размера
 * @param sizes Список размеров массивов для тестирования
 * @param testsPerSize Количество тестов для каждого размера
 * @return Пару списков, содержащих времена замеров
 */
fun runSearchBenchmark(sizes: List<Int>, testsPerSize: Int): Pair<List<Double>, List<Double>> {
    println("Размер массива | Бинарный поиск | Линейный поиск | Ускорение")
    println("---------------|----------------|----------------|----------")

    val binaryTimes = mutableListOf<Double>()
    val linearTimes = mutableListOf<Double>()

    for (size in sizes) {
        // Генерируем отсортированный массив
        val array = generateSortedArray(size)

        // Тестируем разные сценарии поиска
        val testTargets = listOf(
            array.first(),                          // Первый элемент (лучший случай для линейного)
            array.last(),                           // Последний элемент (худший случай для линейного)
            array[size / 2],                        // Средний элемент
            -1,                                     // Отсутствующий элемент (худший случай для обоих)
            array[Random.nextInt(size)]             // Случайный элемент
        )

        var totalBinaryTime = Duration.ZERO
        var totalLinearTime = Duration.ZERO

        for (target in testTargets) {
            totalBinaryTime += measureAverageTime(testsPerSize, ::binarySearch, array, target)
            totalLinearTime += measureAverageTime(testsPerSize, ::linearSearch, array, target)
        }

        // Усредняем по всем тестовым целям
        val avgBinaryTime = totalBinaryTime / testTargets.size
        val avgLinearTime = totalLinearTime / testTargets.size

        binaryTimes.add(avgBinaryTime.inWholeNanoseconds.toDouble())
        linearTimes.add(avgLinearTime.inWholeNanoseconds.toDouble())

        val speedup = avgLinearTime / avgBinaryTime

        println(
            "%13d | %14.3f ms | %14.3f ms | %8.2fx".format(
                size,
                avgBinaryTime.inWholeMilliseconds.toDouble() / 1000,
                avgLinearTime.inWholeMilliseconds.toDouble() / 1000,
                speedup
            )
        )
    }

    // Выводим данные для построения графиков
    println("\nДанные для построения графиков:")
    println("Sizes: ${sizes.joinToString()}")
    println("Binary: [${binaryTimes.joinToString { "%.6f".format(it / 1_000_000) }}]") // в миллисекундах
    println("Linear: [${linearTimes.joinToString { "%.6f".format(it / 1_000_000) }}]") // в миллисекундах

    return Pair(binaryTimes, linearTimes)
}

/**
 * Создает CSV файл для линейного графика.
 * @param sizes Массив размеров массивов для поиска
 * @param binaryTimes Массив замеров времени для бинарного поиска
 * @param linearTimes Массив замеров времени для линейного поиска
 * @param filename Название выходного файла
 */
fun createLinearChartCSV(
    sizes: List<Int>,
    binaryTimes: List<Double>,
    linearTimes: List<Double>,
    filename: String
) {
    val file = File(filename)
    val writer = FileWriter(file)

    try {
        writer.write("Array Size\tBinary Search Time (ns)\tLinear Search Time (ns)\tSpeedup Factor\n")
        for (i in sizes.indices) {
            val size = sizes[i]
            val binaryTime = binaryTimes[i]
            val linearTime = linearTimes[i]
            val speedup = linearTime / binaryTime

            writer.write(
                "$size\t%.6f\t%.6f\t%.2f\n".format(
                    binaryTime, linearTime, speedup
                )
            )
        }

        println("Файл для линейного графика создан: $filename")

    } finally {
        writer.close()
    }
}

/**
 * Создает CSV файл для log-log графика.
 * @param sizes Массив размеров массивов для поиска
 * @param binaryTimes Массив замеров времени для бинарного поиска
 * @param linearTimes Массив замеров времени для линейного поиска
 * @param filename Название выходного файла
 */
fun createLogLogChartCSV(
    sizes: List<Int>,
    binaryTimes: List<Double>,
    linearTimes: List<Double>,
    filename: String
) {
    val file = File(filename)
    val writer = FileWriter(file)

    try {
        writer.write("Array Size\tLog(Array Size)\tBinary Search Time (ns)\tLog(Binary Time)\tLinear Search Time (ns)\tLog(Linear Time)\n")
        for (i in sizes.indices) {
            val size = sizes[i]
            val logSize = ln(size.toDouble())
            val binaryTime = binaryTimes[i]
            val logBinaryTime = ln(binaryTime + 1) // +1 чтобы избежать ln(0)
            val linearTime = linearTimes[i]
            val logLinearTime = ln(linearTime + 1)

            writer.write(
                "$size\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n".format(
                    logSize, binaryTime, logBinaryTime, linearTime, logLinearTime
                )
            )
        }

        println("Файл для log-log графика создан: $filename")

    } finally {
        writer.close()
    }
}

fun main() {
    // Размеры массивов для тестирования
    val sizes = (1..20).map { it * 50000 }
    val testsPerSize = 50
    println("=== СРАВНЕНИЕ АЛГОРИТМОВ ПОИСКА ===")
    println("Количество тестов на размер: $testsPerSize")
    println("Размеры массивов: ${sizes.joinToString()}")
    println()

    val (binaryTimes, linearTimes) = runSearchBenchmark(sizes, testsPerSize)

    // Дополнительный анализ для маленьких массивов
    println("\n=== АНАЛИЗ ДЛЯ МАЛЕНЬКИХ МАССИВОВ ===")
    val smallSizes = listOf(10, 20, 50, 100, 200, 500, 1000)
    runSearchBenchmark(smallSizes, testsPerSize)

    // Создаем директорию для csv-файлов
    val resultsDir = File("search_charts")
    resultsDir.mkdirs()
    // Создаем файлы данных
    createLinearChartCSV(
        sizes, binaryTimes, linearTimes,
        "search_charts/linear_chart_data.csv"
    )

    createLogLogChartCSV(
        sizes, binaryTimes, linearTimes,
        "search_charts/log_log_chart_data.csv"
    )

    println(
        """
            Характеристики ПК:
            Процессор:      AMD Ryzen 7 5800H with Radeon Graphics 3.20 GHz
            ОЗУ:            16,0 ГБ
            ОС:             Windows 11 (x64)
        """.trimIndent()
    )
}