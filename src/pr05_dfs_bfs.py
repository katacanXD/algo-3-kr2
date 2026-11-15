from collections import deque


# --- Задание 1: Обход графа DFS и BFS ---
def task1_dfs_bfs():
    print("=" * 60)
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

    def dfs(v, visited=None, order=None):
        if visited is None:
            visited = set()
            order = []
        visited.add(v)
        order.append(v)
        for nb in graph[v]:
            if nb not in visited:
                dfs(nb, visited, order)
        return order

    def bfs(start):
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

    dfs_order = dfs(1)
    bfs_order = bfs(1)
    print(f"DFS (всего {len(dfs_order)}): {dfs_order}")
    print(f"BFS (всего {len(bfs_order)}): {bfs_order}")


# --- Задание 2: Компоненты связности и двудольность ---
def task2_components_bipartite():
    print("=" * 60)
    print("Задание 2. Компоненты связности и проверка двудольности")
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

    # Поиск компонент связности с помощью DFS
    visited = set()
    components = []
    for v in graph:
        if v not in visited:
            comp = []
            stack = [v]
            while stack:
                cur = stack.pop()
                if cur not in visited:
                    visited.add(cur)
                    comp.append(cur)
                    for nb in graph[cur]:
                        if nb not in visited:
                            stack.append(nb)
            components.append(sorted(comp))

    print("Компоненты связности:", components)

    # Проверка двудольности каждой компоненты через BFS
    for comp in components:
        start = comp[0]
        color = {start: 0}
        queue = deque([start])
        is_bip = True
        while queue and is_bip:
            v = queue.popleft()
            for nb in graph[v]:
                if nb not in color:
                    color[nb] = 1 - color[v]
                    queue.append(nb)
                elif color[nb] == color[v]:
                    is_bip = False
                    break
        if is_bip:
            part0 = [k for k in comp if color[k] == 0]
            part1 = [k for k in comp if color[k] == 1]
            print(f"  Компонента {comp}: двудольная (доля 0: {part0}, доля 1: {part1})")
        else:
            print(f"  Компонента {comp}: НЕ двудольная (содержит нечётный цикл — треугольник A-B-C)")


# --- Задание 3: Топологическая сортировка и кратчайший путь ---
def task3_toposort_and_path():
    print("=" * 60)
    print("Задание 3. Топологическая сортировка и кратчайший путь (A -> H)")
    dag = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["E", "F"],
        "D": ["G"],
        "E": ["G", "H"],
        "F": ["G"],
        "G": ["H"],
        "H": [],
    }

    # Топологическая сортировка через DFS
    visited = set()
    topo = []

    def dfs(v):
        visited.add(v)
        for nb in dag[v]:
            if nb not in visited:
                dfs(nb)
        topo.append(v)

    for v in dag:
        if v not in visited:
            dfs(v)
    topo.reverse()
    print("Топологический порядок:", topo)

    # Кратчайший путь от A до H с помощью BFS
    start, goal = "A", "H"
    prev = {start: None}
    queue = deque([start])
    while queue:
        v = queue.popleft()
        if v == goal:
            break
        for nb in dag[v]:
            if nb not in prev:
                prev[nb] = v
                queue.append(nb)

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    print(f"Кратчайший путь {start} -> {goal}: {' -> '.join(path)} (длина = {len(path) - 1} рёбер)")


if __name__ == "__main__":
    task1_dfs_bfs()
    task2_components_bipartite()
    task3_toposort_and_path()
