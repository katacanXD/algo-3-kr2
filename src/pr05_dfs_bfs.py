import sys
from collections import deque


# обход в глубину рекурсией: вершина попадает в order при первом посещении
def dfs(graph, v, visited=None, order=None):
    if visited is None:
        visited = set()
    if order is None:
        order = []
    visited.add(v)
    order.append(v)
    for nb in graph[v]:
        if nb not in visited:
            dfs(graph, nb, visited, order)
    return order


# обход в ширину: очередь, вершина добавляется по мере обнаружения
def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for nb in graph[v]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return order


def components(graph):
    visited = set()
    result = []
    for v in graph:
        if v not in visited:
            result.append(sorted(dfs(graph, v, visited)))
    return result


# раскраска в два цвета через BFS: конфликт выдаёт нечётный цикл
def color_component(graph, start):
    color = {start: 0}
    dist = {start: 0}
    queue = deque([start])
    while queue:
        v = queue.popleft()
        for nb in graph[v]:
            if nb not in color:
                color[nb] = 1 - color[v]
                dist[nb] = dist[v] + 1
                queue.append(nb)
            elif color[nb] == color[v]:
                return None, (v, nb, dist[v] + dist[nb] + 1)
    return color, None


def topo_sort(graph):
    visited, result = set(), []

    def visit(v):
        visited.add(v)
        for nb in graph[v]:
            if nb not in visited:
                visit(nb)
        result.append(v)

    for v in graph:
        if v not in visited:
            visit(v)
    return result[::-1]


def shortest_path(graph, start, goal):
    prev = {start: None}
    queue = deque([start])
    while queue:
        v = queue.popleft()
        for nb in graph[v]:
            if nb not in prev:
                prev[nb] = v
                queue.append(nb)
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return path[::-1]


def task_1():
    print("Задание 1. Обход графа DFS и BFS от вершины 1")
    graph = {
        1: [2, 3],
        2: [1, 4, 5],
        3: [1, 6, 7],
        4: [2, 8],
        5: [2, 8],
        6: [3, 9],
        7: [3, 9],
        8: [4, 5, 10],
        9: [6, 7, 10],
        10: [8, 9],
    }
    edges = [f"{u}-{v}" for u in graph for v in graph[u] if u < v]
    print("рёбра:", ", ".join(edges))
    by_dfs = dfs(graph, 1)
    by_bfs = bfs(graph, 1)
    print(f"DFS (вершин {len(by_dfs)}): {' '.join(map(str, by_dfs))}")
    print(f"BFS (вершин {len(by_bfs)}): {' '.join(map(str, by_bfs))}")


def task_2():
    print("Задание 2. Компоненты связности и двудольность")
    graph = {
        "A": ["B", "C"],
        "B": ["A", "C"],
        "C": ["A", "B", "D"],
        "D": ["C"],
        "E": ["F"],
        "F": ["E", "G"],
        "G": ["F"],
        "H": [],
        "I": ["J", "L"],
        "J": ["I", "K"],
        "K": ["J", "L"],
        "L": ["I", "K"],
    }
    edges = [f"{u}-{v}" for u in graph for v in graph[u] if u < v]
    print("рёбра:", ", ".join(edges))
    for comp in components(graph):
        name = ", ".join(comp)
        if len(comp) == 1:
            print(f"{name}: двудольная, вершина без рёбер")
            continue
        color, conflict = color_component(graph, comp[0])
        if conflict:
            v, nb, size = conflict
            print(f"{name}: не двудольная, ребро {v}-{nb} замыкает цикл длины {size}")
        else:
            part0 = ", ".join(u for u in comp if color[u] == 0)
            part1 = ", ".join(u for u in comp if color[u] == 1)
            print(f"{name}: двудольная, доли [{part0}] и [{part1}]")


def task_3():
    print("Задание 3. Топологическая сортировка и кратчайший путь A -> H")
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["E", "F"],
        "D": ["G"],
        "E": ["G", "H"],
        "F": ["G"],
        "G": ["H"],
        "H": [],
    }
    print("рёбра:", ", ".join(f"{u}->{v}" for u in graph for v in graph[u]))
    order = topo_sort(graph)
    print("топологический порядок:", " ".join(order))
    path = shortest_path(graph, "A", "H")
    print(f"кратчайший путь A -> H: {' -> '.join(path)} (длина {len(path) - 1})")


TASKS = [task_1, task_2, task_3]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TASKS[int(sys.argv[1]) - 1]()
    else:
        for task in TASKS:
            task()
            print()
