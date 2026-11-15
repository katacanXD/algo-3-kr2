import heapq
import math
import sys


def astar(graph, start, goal, h):
    open_set = [(h[start], start)]
    g = {start: 0}
    came_from = {}
    order = []
    closed = set()
    while open_set:
        _, u = heapq.heappop(open_set)
        if u in closed:
            continue
        closed.add(u)
        order.append(u)
        if u == goal:
            path = [u]
            while u in came_from:
                u = came_from[u]
                path.append(u)
            return path[::-1], g[goal], order
        for v, w in graph[u]:
            ng = g[u] + w
            if v not in g or ng < g[v]:
                g[v] = ng
                came_from[v] = u
                heapq.heappush(open_set, (ng + h[v], v))
    return None, float("inf"), order


def dijkstra_all(graph, start):
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if v not in dist or d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return dist


def astar_grid(grid, start, goal, mode):
    n, m = len(grid), len(grid[0])

    # манхэттенская оценка подходит для четырёх направлений, евклидова - тоже допустимая
    def h(pos):
        dr, dc = abs(pos[0] - goal[0]), abs(pos[1] - goal[1])
        if mode == "manhattan":
            return dr + dc
        if mode == "euclid":
            return math.hypot(dr, dc)
        return 0

    open_set = [(h(start), start)]
    g = {start: 0}
    came_from = {}
    closed = set()
    while open_set:
        _, cur = heapq.heappop(open_set)
        if cur in closed:
            continue
        closed.add(cur)
        if cur == goal:
            path = [cur]
            while cur in came_from:
                cur = came_from[cur]
                path.append(cur)
            return path[::-1], g[goal], len(closed)
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nb = (cur[0] + dr, cur[1] + dc)
            if not (0 <= nb[0] < n and 0 <= nb[1] < m) or grid[nb[0]][nb[1]] == "#":
                continue
            ng = g[cur] + 1
            if nb not in g or ng < g[nb]:
                g[nb] = ng
                came_from[nb] = cur
                heapq.heappush(open_set, (ng + h(nb), nb))
    return None, float("inf"), len(closed)


def print_maze(grid, path):
    for r, row in enumerate(grid):
        cells = ["*" if (r, c) in path and ch == "." else ch for c, ch in enumerate(row)]
        print("   " + " ".join(cells))


def task_1():
    print("Задание 1. A* на взвешенном графе, путь A -> T")
    graph = {
        "A": [("B", 3), ("C", 5)],
        "B": [("A", 3), ("D", 4), ("E", 1)],
        "C": [("A", 5), ("D", 2), ("F", 6)],
        "D": [("B", 4), ("C", 2), ("E", 3), ("G", 8)],
        "E": [("B", 1), ("D", 3), ("H", 5)],
        "F": [("C", 6), ("G", 4)],
        "G": [("D", 8), ("F", 4), ("H", 2), ("T", 1)],
        "H": [("E", 5), ("G", 2), ("T", 6)],
        "T": [("G", 1), ("H", 6)],
    }
    # условные координаты вершин: по ним считается манхэттенская эвристика
    coords = {"A": (0, 2), "B": (2, 0), "C": (2, 4), "D": (3, 1),
              "E": (3, 0), "F": (4, 4), "G": (5, 2), "H": (5, 0), "T": (6, 2)}
    tx, ty = coords["T"]
    h = {v: abs(x - tx) + abs(y - ty) for v, (x, y) in coords.items()}
    true = dijkstra_all(graph, "T")

    print("h по Манхэттену: " + ", ".join(f"{v}={h[v]}" for v in "ABCDEFGHT"))
    print("истинные d(v,T): " + ", ".join(f"{v}={true[v]}" for v in "ABCDEFGHT"))
    over = [v for v in graph if h[v] > true[v]]
    print("допустимость h(v) <= d(v,T): " + ("нарушена у " + ", ".join(over) if over else "выполняется"))

    path, cost, order = astar(graph, "A", "T", h)
    path_d, cost_d, order_d = astar(graph, "A", "T", {v: 0 for v in graph})
    print(f"A*:       {' -> '.join(path)}, стоимость {cost}, исследовано вершин {len(order)}")
    print(f"Дейкстра: {' -> '.join(path_d)}, стоимость {cost_d}, исследовано вершин {len(order_d)}")


def task_2():
    print("Задание 2. A* в лабиринте 8x8")
    maze = [
        "S..#....",
        ".#.#.##.",
        ".#....#.",
        ".####.#.",
        "....#...",
        "###.###.",
        "........",
        ".#####.G",
    ]
    path, cost, explored = astar_grid(maze, (0, 0), (7, 7), "manhattan")
    path_e, cost_e, explored_e = astar_grid(maze, (0, 0), (7, 7), "euclid")
    _, cost_d, explored_d = astar_grid(maze, (0, 0), (7, 7), "zero")

    print(f"A* (Манхэттен): длина пути {cost}, исследовано клеток {explored}")
    print_maze(maze, path)
    same = "путь совпал" if path_e == path else "путь другой"
    print(f"A* (Евклид): длина пути {cost_e}, исследовано клеток {explored_e}, {same}")
    print(f"Дейкстра: длина пути {cost_d}, исследовано клеток {explored_d}")


def task_3():
    print("Задание 3. A* с эвристикой из условия, путь A -> T")
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
    true = dijkstra_all(graph, "T")

    print("d(v,T): " + ", ".join(f"{v}={true[v]}" for v in "ABCDEFGHT"))
    print("h(v) <= d(v,T): " + ", ".join(f"{v} {h[v]}<={true[v]}" for v in "ABCDEFGH"))
    over = [v for v in graph if h[v] > true[v]]
    print("переоценки: " + (", ".join(over) if over else "нет, эвристика допустима"))

    path, cost, order = astar(graph, "A", "T", h)
    path_0, cost_0, order_0 = astar(graph, "A", "T", {v: 0 for v in graph})
    print(f"A*:     {' -> '.join(path)}, стоимость {cost}, исследовано вершин {len(order)}")
    print("        порядок: " + ", ".join(order))
    print(f"h = 0:  {' -> '.join(path_0)}, стоимость {cost_0}, исследовано вершин {len(order_0)}")
    print("        порядок: " + ", ".join(order_0))


TASKS = [task_1, task_2, task_3]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TASKS[int(sys.argv[1]) - 1]()
    else:
        for task in TASKS:
            task()
            print()
