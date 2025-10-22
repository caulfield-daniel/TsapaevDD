import org.jetbrains.letsPlot.export.ggsave
import org.jetbrains.letsPlot.geom.geomLine
import org.jetbrains.letsPlot.geom.geomPoint
import org.jetbrains.letsPlot.label.ggtitle
import org.jetbrains.letsPlot.label.xlab
import org.jetbrains.letsPlot.label.ylab
import org.jetbrains.letsPlot.letsPlot

/**
 * Создаёт графики сравнения производительности на основе результатов тестирования.
 * @param results список результатов тестирования
 */
fun createCharts(results: List<PerformanceResult>): Boolean {
    return try {
        // Конвертируем в миллисекунды
        val resultsInMs = results.map { it.copy(timeNs = it.timeNs / 1_000_000.0) }

        // График для вставки в начало
        val insertionData = resultsInMs.filter { it.operation == "Вставка в начало" }
        val insertionPlot = letsPlot(
            mapOf(
                "elements" to insertionData.map { it.elements },
                "time" to insertionData.map { it.timeNs },
                "structure" to insertionData.map { it.dataStructure }
            )
        ) + geomLine { x = "elements"; y = "time"; color = "structure" } +
                geomPoint { x = "elements"; y = "time"; color = "structure" } +
                ggtitle("Вставка в начало") +
                xlab("Количество элементов") +
                ylab("Время (мс)")

        ggsave(insertionPlot, "performance_insertion.png")

        // График для удаления из начала
        val removalData = resultsInMs.filter { it.operation == "Удаление из начала" }
        val removalPlot = letsPlot(
            mapOf(
                "elements" to removalData.map { it.elements },
                "time" to removalData.map { it.timeNs },
                "structure" to removalData.map { it.dataStructure }
            )
        ) + geomLine { x = "elements"; y = "time"; color = "structure" } +
                geomPoint { x = "elements"; y = "time"; color = "structure" } +
                ggtitle("Удаление из начала") +
                xlab("Количество элементов") +
                ylab("Время (мс)")

        ggsave(removalPlot, "performance_removal.png")

        true
    } catch (e: Exception) {
        println("Ошибка при построении графиков с помощью Lets-Plot: ${e.message}")
        false
    }
}

/**
 * Выводит результаты тестирования в виде таблицы в консоль.
 * @param results список результатов тестирования
 */
fun printBenchmarkTable(results: List<PerformanceResult>) {
    println("Результаты измерений производительности:")
    println("========================================")
    println("Операция            | Структура    | Элементы | Время(нс)")
    println("--------------------|--------------|----------|----------")

    results.groupBy { it.operation }.forEach { (operation, opResults) ->
        println("$operation:")
        opResults.sortedBy { it.elements }.forEach { result ->
            println(
                "                    | %-12s | %8d | %8.1f".format(
                    result.dataStructure, result.elements, result.timeNs
                )
            )
        }
        println()
    }
}