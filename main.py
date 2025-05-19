from queue import Queue # Для обхода в ширину
import random


class Node:
    '''
    Класс для хранения единичного узла бинарного дерева
    '''
    def __init__(self, val):
        self.l = None  # Связь с левым потомком
        self.r = None  # Связь с правым потомком
        self.v = val   # Ключ (значение, которое хранится в узле)

class Tree:
    '''
    Класс для хранения бинарного дерева поиска
    '''
    def __init__(self):
        '''
        Создаем пустое дерево
        '''
        self.root = None

    def getRoot(self):
        '''
        Получение значения корня
        '''
        return self.root

    def add(self, val):
        '''
        Добавление узла.
        Если дерево не содержит элементов, создаем дерево из одного элемента.
        Если дерево не пустое, вызываем вспомогательную функцию добавления.
        '''
        if self.root is None:
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        '''
        Вспомогательная рекурсивная функция добавления.
        Если элемент меньше значения текущего узла,
        добавляем его в левое поддерево.
        В противном случае добавляем его в правое поддерево.
        '''
        if val < node.v:
            if node.l is not None:
                self._add(val, node.l)
            else:
                node.l = Node(val)
        else:
            if node.r is not None:
                self._add(val, node.r)
            else:
                node.r = Node(val)

    def find(self, val):
        '''
        Поиск узла.
        Если узел не пуст, вызываем вспомогательную функцию поиска,
        иначе возвращаем None.
        '''
        if self.root is not None:
            return self._find(val, self.root)
        else:
            return None

    def _find(self, val, node):
        '''
        Вспомогательная рекурсивная функция поиска.
        Если узел найден, возвращаем его. Если значение узла больше искомого,
        продолжаем поиск в левом поддереве, если оно не пустое. Если значение
        узла меньше искомого, продолжаем поиск в правом поддереве,
        если оно не пустое.
        '''
        if val == node.v:
            return node.v
        elif (val < node.v and node.l != None):
            return self._find(val, node.l)
        elif (val > node.v and node.r != None):
            return self._find(val, node.r)

    def deleteTree(self):
        '''
        Удаление дерева.
        Удаляем корень, все остальное делает сборщик мусора.
        '''
        self.root = None

    def printTree(self):
        '''
        Печать дерева.
        Вызываем вспомогательную функцию печати.
        '''
        if self.root is not None:
            print("Дерево:")
            self._printTree(self.root)
            print()
        else:
            print("Дерево не существует")

    def _printTree(self, node):
        '''
        Вспомогательная рекурсивная функция печати.
        '''
        if node is not None:
            print(str(node.v), end=' ')
            self._printTree(node.l)
            self._printTree(node.r)

    def BFS(self):
        '''
        Обход дерева в ширину.
        '''
        if self.root is not None:
            q = Queue()
            q.put(self.root)
            while not q.empty():
                x = q.get()
                print(str(x.v), end=' ')
                if x.l is not None:
                     q.put(x.l)
                if x.r is not None:
                     q.put(x.r)
            print()
        else:
            print("Дерево не существует")

    # Задача 2: Метод для вычисления количества узлов
    def countNodes(self):
        '''
        Возвращает количество узлов в дереве
        '''
        return self._countNodes(self.root)

    def _countNodes(self, node):
        '''
        Вспомогательная рекурсивная функция для подсчета узлов
        '''
        if node is None:
            return 0
        return 1 + self._countNodes(node.l) + self._countNodes(node.r)

    # Задача 3: Метод для вычисления количества листьев
    def countLeaves(self):
        '''
        Возвращает количество листьев в дереве
        '''
        return self._countLeaves(self.root)

    def _countLeaves(self, node):
        '''
        Вспомогательная рекурсивная функция для подсчета листьев
        '''
        if node is None:
            return 0
        if node.l is None and node.r is None:
            return 1
        return self._countLeaves(node.l) + self._countLeaves(node.r)

    # Задача 4: Метод для вычисления высоты дерева
    def height(self):
        '''
        Возвращает высоту дерева
        '''
        return self._height(self.root)

    def _height(self, node):
        '''
        Вспомогательная рекурсивная функция для вычисления высоты
        '''
        if node is None:
            return 0
        left_height = self._height(node.l)
        right_height = self._height(node.r)
        return max(left_height, right_height) + 1

    # Задача 5: Метод обхода в глубину с использованием стека
    def DFS(self):
        '''
        Обход дерева в глубину с использованием стека
        '''
        if self.root is None:
            print("Дерево не существует")
            return

        stack = []
        stack.append(self.root)

        while stack:
            node = stack.pop()
            print(str(node.v), end=' ')

            # Сначала добавляем правый потомок, чтобы левый обрабатывался первым
            if node.r is not None:
                stack.append(node.r)
            if node.l is not None:
                stack.append(node.l)
        print()

    # Задача 6*: Красивый вывод дерева
    def prettyPrint(self):
        '''
        Красивый вывод дерева в виде древовидной структуры
        '''
        if self.root is None:
            print("Дерево не существует")
            return

        levels = []
        q = Queue()
        q.put((self.root, 0))

        # Собираем узлы по уровням
        while not q.empty():
            node, level = q.get()

            if level == len(levels):
                levels.append([])

            levels[level].append(str(node.v) if node else " ")

            if node:
                q.put((node.l, level + 1))
                q.put((node.r, level + 1))

        # Удаляем пустые уровни (если есть)
        levels = [level for level in levels if any(node != " " for node in level)]

        # Выводим дерево
        for i, level in enumerate(levels):
            indent = " " * (2 ** (len(levels) - i - 1) - 1)
            separator = " " * (2 ** (len(levels) - i) - 1)
            print(indent + separator.join(level))
trea = Tree()
n = 10  # количество чисел
min_val = 1
max_val = 100

numbers = [random.randint(min_val, max_val) for _ in range(n)]
print("Сгенерированные числа:", numbers)

for num in numbers:
    trea.add(num)

# Задача 2: Количество узлов
print("Количество узлов:", trea.countNodes())

# Задача 3: Количество листьев
print("Количество листьев:", trea.countLeaves())

# Задача 4: Высота дерева
print("Высота дерева:", trea.height())

# Задача 5: Обход в глубину
print("Обход в глубину (DFS):", end=' ')
trea.DFS()

# Задача 6: Красивый вывод
print("\nКрасивый вывод дерева:")
trea.prettyPrint()