import java.util.*

/**
 * Проверяет, является ли строка сбалансированной по скобкам.
 * Временная сложность: O(n), где n — длина строки.
 * @param str входная строка, содержащая скобки
 * @return true, если все скобки сбалансированы, иначе false
 */
fun isBalancedParentheses(str: String): Boolean {
    val stack = mutableListOf<Char>()
    val pairs = mapOf(')' to '(', ']' to '[', '}' to '{')

    for (char in str) {
        when (char) {
            '(', '[', '{' -> stack.add(char)
            ')', ']', '}' -> {
                if (stack.isEmpty() || stack.removeAt(stack.size - 1) != pairs[char]) return false
            }
        }
    }
    return stack.isEmpty()
}

/**
 * Класс, имитирующий очередь печати документов.
 * Использует двустороннюю очередь ArrayDeque для хранения задач.
 */
class PrintQueue {
    private val queue = ArrayDeque<String>()

    /**
     * Добавляет задание в конец очереди.
     * @param job имя документа для печати
     */
    fun addJob(job: String) = queue.addLast(job)

    /**
     * Обрабатывает следующее задание из начала очереди.
     * @return имя обработанного документа или null, если очередь пуста
     */
    fun processNext(): String? = queue.pollFirst()

    /**
     * Проверяет, есть ли задания в очереди.
     * @return true, если очередь не пуста
     */
    fun hasJobs() = queue.isNotEmpty()

    /**
     * Возвращает количество заданий в очереди.
     * @return текущее количество документов в очереди
     */
    fun jobsCount() = queue.size
}

/**
 * Проверяет, является ли строка палиндромом.
 * Временная сложность: O(n), где n — длина строки.
 * @param str входная строка
 * @return true, если строка является палиндромом
 */
fun isPalindrome(str: String): Boolean {
    val deque = ArrayDeque<Char>().apply {
        str.forEach { addLast(it) }
    }

    while (deque.size > 1) {
        if (deque.pollFirst() != deque.pollLast()) return false
    }
    return true
}

/**
 * Точка входа. Выполняет тестирование всех функций.
 */
fun main() {
    // Тест проверки сбалансированности скобок
    println("Проверка скобок:")
    println("(([])): ${isBalancedParentheses("(([]))")}") // true
    println("([)]: ${isBalancedParentheses("([)]")}")     // false

    // Тест очереди печати
    val printQueue = PrintQueue().apply {
        addJob("Document1")
        addJob("Document2")
        addJob("Document3")
    }
    println("\nОчередь печати (документов: ${printQueue.jobsCount()}):")
    while (printQueue.hasJobs()) {
        println("Обрабатывается: ${printQueue.processNext()}")
    }

    // Тест проверки палиндромов
    println("\nПроверка палиндромов:")
    println("racecar: ${isPalindrome("racecar")}") // true
    println("hello: ${isPalindrome("hello")}")     // false
    println("a: ${isPalindrome("a")}")             // true
}