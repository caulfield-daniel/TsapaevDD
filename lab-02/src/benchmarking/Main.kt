/**
 * Точка входа в программу. Запускает тестирование, создание графиков и вывод результатов.
 */
fun main() {
    println("Измерение производительности структур данных...")
    val results = measurePerformance()

    println("Создание графиков...")
    createCharts(results)

    printBenchmarkTable(results)

    println("Графики сохранены в файлы:")
    println("- performance_insertion.png")
    println("- performance_removal.png")
    println("\nАнализ завершен!")

}