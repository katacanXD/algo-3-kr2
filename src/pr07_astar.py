import heapq
import math


def dijkstra_all(graph, start):
    """Дейкстра от вершины start до всех вершин (для проверки допустимости)."""
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def astar_graph(graph, start, goal, h_dict):
    """Простая реализация A* для взвешенного графа с подсчётом исследованных вершин."""
    open_set = [(h_dict[start], start)]
    g_score = {start: 0}
    came_from = {}
    explored = []
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)
        explored.append(current)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1], g_score[goal], explored

        for nb, w in graph[current]:
            tentative_g = g_score[current] + w
            if nb not in g_score or tentative_g < g_score[nb]:
                came_from[nb] = current
                g_score[nb] = tentative_g
                f = tentative_g + h_dict[nb]
                heapq.heappush(open_set, (f, nb))

    return None, float("inf"), explored


# --- Задание 1: A* на взвешенном графе ---
def task1_weighted_astar():
    print("=" * 60)
    print("Задание 1. A* на взвешенном графе (A -> T)")
    graph = {
        "A": [("B", 3), ("C", 5)],
        "B": [("A", 3), ("D", 4), ("E", 7)],
        "C": [("A", 5), ("D", 2), ("F", 6)],
        "D": [("B", 4), ("C", 2), ("E", 3), ("G", 8)],
        "E": [("B", 7), ("D", 3), ("H", 5)],
        "F": [("C", 6), ("G", 4)],
        "G": [("D", 8), ("F", 4), ("H", 2), ("T", 7)],
        "H": [("E", 5), ("G", 2), ("T", 6)],
        "T": [("G", 7), ("H", 6)],
    }
    coords = {
        "A": (0, 6), "B": (4, 10), "C": (5, 3),
        "D": (8, 6), "E": (8, 10), "F": (9, 3),
        "G": (12, 4), "H": (12, 10), "T": (15, 8),
    }
    tx, ty = coords["T"]
    h = {v: abs(x - tx) + abs(y - ty) for v, (x, y) in coords.items()}

    true_dist = dijkstra_all(graph, "T")
    admissible = all(h[v] <= true_dist[v] for v in graph)
    print("Манхэттенская эвристика h:", h)
    print("Истинные расстояния до T:", {v: true_dist[v] for v in sorted(graph)})
    print("Эвристика допустима (h(v) <= d(v, T)):", admissible)

    path_a, cost_a, exp_a = astar_graph(graph, "A", "T", h)
    h_zero = {v: 0 for v in graph}
    path_d, cost_d, exp_d = astar_graph(graph, "A", "T", h_zero)

    print(f"A*:       путь = {' -> '.join(path_a)}, стоимость = {cost_a}, исследовано = {len(exp_a)} {exp_a}")
    print(f"Дейкстра: путь = {' -> '.join(path_d)}, стоимость = {cost_d}, исследовано = {len(exp_d)} {exp_d}")


# --- Задание 2: Лабиринт 8x8 ---
def task2_maze_8x8():
    print("=" * 60)
    print("Задание 2. A* в лабиринте 8x8")
    grid = [
        "S..#....",
        ".#.#.##.",
        ".#....#.",
        ".####.#.",
        "....#...",
        "###.###.",
        "........",
        ".#####.G",
    ]
    n, m = len(grid), len(grid[0])
    start, goal = (0, 0), (7, 7)

    def search_grid(mode):
        def h(pos):
            dr = abs(pos[0] - goal[0])
            dc = abs(pos[1] - goal[1])
            if mode == "manhattan":
                return dr + dc
            if mode == "euclidean":
                return math.hypot(dr, dc)
            return 0  # Дейкстра

        open_set = [(h(start), start)]
        g_score = {start: 0}
        came_from = {}
        visited = set()

        while open_set:
            _, cur = heapq.heappop(open_set)
            if cur in visited:
                continue
            visited.add(cur)
            if cur == goal:
                path = [cur]
                while cur in came_from:
                    cur = came_from[cur]
                    path.append(cur)
                return path[::-1], g_score[goal], len(visited)

            r, c = cur
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != "#":
                    nb = (nr, nc)
                    tg = g_score[cur] + 1
                    if nb not in g_score or tg < g_score[nb]:
                        came_from[nb] = cur
                        g_score[nb] = tg
                        heapq.heappush(open_set, (tg + h(nb), nb))
        return None, float("inf"), len(visited)

    for mode, label in [("manhattan", "A* (Манхэттен)"), ("euclidean", "A* (Евклид)"), ("dijkstra", "Дейкстра (h=0)")]:
        path, length, explored = search_grid(mode)
        print(f"{label}: длина = {length}, исследовано клеток = {explored}")
        print(f"  Путь: {path}")


# --- Задание 3: A* с заданной эвристикой ---
def task3_given_heuristic():
    print("=" * 60)
    print("Задание 3. Проверка эвристики и сравнение A* с Дейкстрой")
    graph = {
        "A": [("B", 2), ("C", 4)],
        "B": [("A", 2), ("D", 5)],
        "C": [("A", 4), ("D", 1), ("E", 7)],
        "D": [("B", 5), ("C", 1), ("F", 3)],
        "E": [("C", 7), ("F", 2), ("G", 6)],
        "F": [("D", 3), ("E", 2), ("H", 4)],
        "G": [("E", 6), ("H", 3)],
        "H": [("F", 4), ("G", 3), ("T", 5)],
        "T": [("H", 5)],
    }
    h = {"A": 8, "B": 7, "C": 6, "D": 5, "E": 4, "F": 3, "G": 3, "H": 2, "T": 0}

    true_dist = dijkstra_all(graph, "T")
    print("Проверка допустимости (h(v) <= d(v, T)):")
    bad = []
    for v in sorted(graph):
        ok = h[v] <= true_dist[v]
        if not ok:
            bad.append(v)
        print(f"  {v}: h={h[v]}, d={true_dist[v]} -> {'допустима' if ok else 'ПЕРЕОЦЕНКА'}")
    print("Недопустимые вершины:", bad if bad else "нет (все допустимы)")

    path_a, cost_a, exp_a = astar_graph(graph, "A", "T", h)
    path_0, cost_0, exp_0 = astar_graph(graph, "A", "T", {v: 0 for v in graph})

    print(f"A* (заданная h): путь = {' -> '.join(path_a)}, стоимость = {cost_a}")
    print(f"  Исследовано ({len(exp_a)}): {exp_a}")
    print(f"A* (h = 0 / Дейкстра): путь = {' -> '.join(path_0)}, стоимость = {cost_0}")
    print(f"  Исследовано ({len(exp_0)}): {exp_0}")


if __name__ == "__main__":
    task1_weighted_astar()
    task2_maze_8x8()
    task3_given_heuristic()
