import heapq
from collections import defaultdict, deque


class Graph:
    def __init__(self, filename=None, directed=False):
        """
        Инициализация графа.
        Если указан filename, загружает граф из файла.
        Параметр directed указывает, является ли граф ориентированным.
        """
        self.directed = directed
        self.vertices = set()
        self.edges = []
        self.adjacency_list = defaultdict(list)
        self.adjacency_matrix = None
        self.incidence_matrix = None

        if filename:
            self.load_from_file(filename)

    def load_from_file(self, filename):
        """
        Загрузка графа из файла.
        Формат файла:
        Первая строка: количество вершин (опционально)
        Последующие строки: пары вершин (ребра), возможно с весом
        """
        with open(filename, 'r') as f:
            lines = f.readlines()

            # Пропускаем пустые строки
            lines = [line.strip() for line in lines if line.strip()]

            # Читаем ребра
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    u = parts[0]
                    v = parts[1]
                    weight = float(parts[2]) if len(parts) > 2 else 1.0

                    self.vertices.add(u)
                    self.vertices.add(v)
                    self.edges.append((u, v, weight))
                    self.adjacency_list[u].append((v, weight))

                    if not self.directed:
                        self.adjacency_list[v].append((u, weight))

        # После загрузки ребер строим матричные представления
        self._build_matrix_representations()

    def _build_matrix_representations(self):
        """Строит матричные представления графа"""
        vertices = sorted(self.vertices)
        n = len(vertices)
        m = len(self.edges)

        # Матрица смежности
        self.adjacency_matrix = [[0] * n for _ in range(n)]
        vertex_index = {v: i for i, v in enumerate(vertices)}

        for u, v, weight in self.edges:
            i = vertex_index[u]
            j = vertex_index[v]
            self.adjacency_matrix[i][j] = weight
            if not self.directed:
                self.adjacency_matrix[j][i] = weight

        # Матрица инцидентности
        self.incidence_matrix = [[0] * m for _ in range(n)]

        for edge_idx, (u, v, weight) in enumerate(self.edges):
            i = vertex_index[u]
            j = vertex_index[v]
            self.incidence_matrix[i][edge_idx] = weight
            if self.directed:
                self.incidence_matrix[j][edge_idx] = -weight
            else:
                self.incidence_matrix[j][edge_idx] = weight

    def get_adjacency_matrix(self):
        """Возвращает матрицу смежности"""
        if not self.incidence_matrix:
            print("Матрица инцидентности не построена")
            return

        vertices = sorted(self.vertices)
        edges = self.edges
        n = len(vertices)
        m = len(edges)

        print("\nМатрица инцидентности (по столбцам):")
        print("   " + " ".join(f"{i + 1:>5}" for i in range(m)))

        # Транспонируем матрицу для вывода по столбцам
        transposed = [[self.incidence_matrix[j][i] for j in range(n)] for i in range(m)]

        for i in range(n):
            print(f"{vertices[i]:>3}", end=" ")
            for j in range(m):
                print(f"{transposed[j][i]:>5}", end=" ")
            print()
        return print("_________________________________")

    def get_incidence_matrix(self):
        """Возвращает матрицу инцидентности"""
        if not self.incidence_matrix:
            print("Матрица инцидентности не построена")
            return

        vertices = sorted(self.vertices)
        edges = self.edges
        n = len(vertices)
        m = len(edges)

        print("   " + " ".join(f"{i + 1:>5}" for i in range(m)))

        # Транспонируем матрицу для вывода по столбцам
        transposed = [[self.incidence_matrix[j][i] for j in range(n)] for i in range(m)]

        for i in range(n):
            print(f"{vertices[i]:>3}", end=" ")
            for j in range(m):
                print(f"{transposed[j][i]:>5}", end=" ")
            print()

    def get_edge_list(self):
        """Возвращает список ребер"""
        return self.edges

    def get_adjacency_list(self):
        """Возвращает список смежности"""
        return self.adjacency_list

    def kruskal_mst(self):
        """
        Алгоритм Краскала для поиска минимального остовного дерева.
        Возвращает список ребер MST.
        """
        parent = {}
        rank = {}

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(u, v):
            root_u = find(u)
            root_v = find(v)

            if root_u == root_v:
                return False

            if rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            elif rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            else:
                parent[root_v] = root_u
                rank[root_u] += 1
            return True

        # Инициализация
        for v in self.vertices:
            parent[v] = v
            rank[v] = 0

        # Сортируем ребра по весу
        sorted_edges = sorted(self.edges, key=lambda x: x[2])
        mst = []

        for u, v, weight in sorted_edges:
            if union(u, v):
                mst.append((u, v, weight))
                if len(mst) == len(self.vertices) - 1:
                    break

        return mst

    def has_eulerian_cycle(self):
        """
        Проверяет, содержит ли граф Эйлеров цикл.
        Для неориентированного графа:
        - все вершины должны иметь четную степень
        - граф должен быть связным
        Для ориентированного графа:
        - для всех вершин in_degree == out_degree
        - граф должен быть сильно связным
        """
        if not self.directed:
            # Проверяем степени вершин
            degrees = defaultdict(int)
            for u in self.adjacency_list:
                degrees[u] += len(self.adjacency_list[u])
                for v, _ in self.adjacency_list[u]:
                    degrees[v] += 1

            for v in self.vertices:
                if degrees[v] % 2 != 0:
                    return False

            # Проверяем связность (упрощенная проверка)
            if not self._is_connected():
                return False
        else:
            # Для ориентированного графа
            in_degree = defaultdict(int)
            out_degree = defaultdict(int)

            for u in self.adjacency_list:
                out_degree[u] += len(self.adjacency_list[u])
                for v, _ in self.adjacency_list[u]:
                    in_degree[v] += 1

            for v in self.vertices:
                if in_degree[v] != out_degree[v]:
                    return False

            # Проверка сильной связности (упрощенная)
            if not self._is_strongly_connected():
                return False

        return True

    def _is_connected(self):
        """Проверяет, является ли неориентированный граф связным"""
        if not self.vertices:
            return True

        visited = set()
        stack = [next(iter(self.vertices))]

        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                for neighbor, _ in self.adjacency_list[v]:
                    stack.append(neighbor)

        return len(visited) == len(self.vertices)

    def _is_strongly_connected(self):
        """Проверяет, является ли ориентированный граф сильно связным"""
        if not self.vertices:
            return True

        # Проверяем достижимость всех вершин из первой
        start = next(iter(self.vertices))
        visited = set()
        stack = [start]

        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                for neighbor, _ in self.adjacency_list[v]:
                    stack.append(neighbor)

        if len(visited) != len(self.vertices):
            return False

        # Транспонируем граф
        reversed_adj = defaultdict(list)
        for u in self.adjacency_list:
            for v, weight in self.adjacency_list[u]:
                reversed_adj[v].append((u, weight))

        # Проверяем достижимость всех вершин в транспонированном графе
        visited = set()
        stack = [start]

        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                for neighbor, _ in reversed_adj[v]:
                    stack.append(neighbor)

        return len(visited) == len(self.vertices)

    def dijkstra(self, start):
        """
        Алгоритм Дейкстры для поиска кратчайших путей от заданной вершины.
        Возвращает словарь расстояний до всех вершин.
        """
        distances = {v: float('inf') for v in self.vertices}
        distances[start] = 0
        heap = [(0, start)]

        while heap:
            current_dist, u = heapq.heappop(heap)

            if current_dist > distances[u]:
                continue

            for v, weight in self.adjacency_list[u]:
                distance = current_dist + weight
                if distance < distances[v]:
                    distances[v] = distance
                    heapq.heappush(heap, (distance, v))

        return distances

    def floyd_warshall(self):
        """
        Алгоритм Флойда-Уоршелла для поиска кратчайших путей между всеми парами вершин.
        Возвращает матрицу кратчайших расстояний.
        """
        vertices = sorted(self.vertices)
        n = len(vertices)
        vertex_index = {v: i for i, v in enumerate(vertices)}

        # Инициализация матрицы расстояний
        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0

        # Заполнение известными расстояниями
        for u, v, weight in self.edges:
            i = vertex_index[u]
            j = vertex_index[v]
            if weight < dist[i][j]:
                dist[i][j] = weight
                if not self.directed:
                    dist[j][i] = weight

        # Алгоритм Флойда-Уоршелла
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return dist


    def print_incidence_matrix_by_columns(self):
        """Выводит матрицу инцидентности по столбцам"""
        if not self.incidence_matrix:
            print("Матрица инцидентности не построена")
            return

        vertices = sorted(self.vertices)
        edges = self.edges
        n = len(vertices)
        m = len(edges)

        print("\nМатрица инцидентности (по столбцам):")
        print("   " + " ".join(f"E{i + 1:>5}" for i in range(m)))

        # Транспонируем матрицу для вывода по столбцам
        transposed = [[self.incidence_matrix[j][i] for j in range(n)] for i in range(m)]

        for i in range(n):
            print(f"{vertices[i]:>3}", end=" ")
            for j in range(m):
                print(f"{transposed[j][i]:>5}", end=" ")
            print()
graph = Graph("graph.txt", directed=False)
# Задача 1: Различные представления графа
print("Матрица смежности:")
print(graph.get_adjacency_matrix())

print("\nМатрица инцидентности:")
print(graph.get_incidence_matrix())

print("\nСписок ребер:")
print(graph.get_edge_list())

print("\nСписок смежности:")
print(dict(graph.get_adjacency_list()))

# Задача 2: Минимальное остовное дерево (алгоритм Краскала)
print("\nМинимальное остовное дерево (Краскал):")
mst = graph.kruskal_mst()
for edge in mst:
    print(f"{edge[0]} - {edge[1]}: {edge[2]}")

# Задача 3: Проверка на Эйлеров цикл
print("\nГраф содержит Эйлеров цикл:", graph.has_eulerian_cycle())

# Задача 4: Кратчайшие пути от заданной вершины (алгоритм Дейкстры)
start_vertex = "A"  # Пример вершины
print(f"\nКратчайшие пути от вершины {start_vertex}:")
distances = graph.dijkstra(start_vertex)
for v, dist in distances.items():
    print(f"До {v}: {dist}")

# Задача 5: Матрица кратчайших путей (алгоритм Флойда-Уоршелла)
print("\nМатрица кратчайших путей (Флойд-Уоршелл):")
floyd_matrix = graph.floyd_warshall()
for row in floyd_matrix:
    print(row)