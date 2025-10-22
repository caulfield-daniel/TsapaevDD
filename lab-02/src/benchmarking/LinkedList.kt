/**
 * Класс узла связанного списка.
 * @property data данные, хранящиеся в узле
 * @property next ссылка на следующий узел
 */
class Node<T>(var data: T, var next: Node<T>? = null)

/**
 * Реализация односвязного списка.
 * @property head ссылка на первый элемент списка
 * @property tail ссылка на последний элемент списка
 */
class LinkedList<T> {
    private var head: Node<T>? = null
    private var tail: Node<T>? = null

    /**
     * Добавляет новый элемент в начало списка.
     * Временная сложность: O(1)
     * @param data данные для добавления
     */
    fun insertAtStart(data: T) {
        val newNode = Node(data, head)
        head = newNode
        if (tail == null) tail = head
    }

    /**
     * Добавляет новый элемент в конец списка.
     * Временная сложность: O(1), благодаря использованию tail.
     * @param data данные для добавления
     */
    fun insertAtEnd(data: T) {
        val newNode = Node(data)
        if (tail == null) {
            head = newNode
            tail = newNode
        } else {
            tail!!.next = newNode
            tail = newNode
        }
    }

    /**
     * Удаляет элемент из начала списка.
     * Временная сложность: O(1)
     * @return данные удаленного элемента или null, если список пуст
     */
    fun deleteFromStart(): T? {
        val value = head?.data
        head = head?.next
        if (head == null) tail = null
        return value
    }

    /**
     * Проходит по списку и возвращает все элементы в виде списка.
     * Временная сложность: O(n), где n — количество элементов в списке
     * @return список данных
     */
    fun traverse(): List<T> {
        val elements = mutableListOf<T>()
        var current = head
        while (current != null) {
            elements.add(current.data)
            current = current.next
        }
        return elements
    }
}