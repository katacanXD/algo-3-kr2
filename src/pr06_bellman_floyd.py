import math
import sys


# V-1 проход по всем рёбрам; если на очередном проходе ничего не улучшилось, дальше смысла нет
def bellman_ford(names, edges, start):
    dist = {name: math.inf for name in names}
    prev = {name: None for name in names}
    dist[start] = 0
    for _ in range(len(names) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                changed = True
        if not changed:
            break
    return dist, prev


def restore_path(prev, target):
    path = []
    v = target
    while v is not None:
        path.append(v)
        v = prev[v]
    return path[::-1]


def floyd(n, matrix):
    dist = [row[:] for row in matrix]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def show_matrix(dist, names):
    print("      " + " ".join(f"{name:>4}" for name in names))
    for i, name in enumerate(names):
        row = " ".join(f"{'inf' if v == math.inf else v:>4}" for v in dist[i])
        print(f"{name:>4}  {row}")


def task_1():
    print("Задание 1. Беллман-Форд: расстояния от S и путь до T")
    names = ["S", "A", "B", "C", "D", "T"]
    edges = [
        ("S", "A", 4),
        ("S", "B", 3),
        ("A", "B", -2),
        ("A", "C", 7),
        ("B", "C", 5),
        ("B", "D", 8),
        ("C", "D", -1),
        ("C", "T", 6),
        ("D", "T", 3),
    ]
    dist, prev = bellman_ford(names, edges, "S")
    print("расстояния: " + ", ".join(f"{name}={dist[name]:g}" for name in names))
    print(f"путь S -> T: {' -> '.join(restore_path(prev, 'T'))}, длина {dist['T']:g}")
    loop = [f"{u}->{v}" for u, v, w in edges if dist[u] + w < dist[v]]
    print("отрицательный цикл: " + (", ".join(loop) if loop else "нет"))


def task_2():
    print("Задание 2. Флойд-Уоршелл: расстояния между всеми парами")
    names = ["1", "2", "3", "4", "5"]
    edges = [
        (0, 1, 5), (0, 2, 10), (1, 2, 3), (1, 3, -2),
        (2, 3, 2), (2, 4, 7), (3, 4, 4), (4, 0, 12),
    ]
    n = len(names)
    matrix = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0
    for u, v, w in edges:
        matrix[u][v] = w

    dist = floyd(n, matrix)
    show_matrix(dist, names)
    loop = [names[i] for i in range(n) if dist[i][i] < 0]
    print("отрицательный цикл: " + (", ".join(loop) if loop else "нет"))


def task_3():
    print("Задание 3. Арбитраж валют")
    names = ["USD", "EUR", "GBP", "JPY"]
    rates = [
        ("USD", "EUR", 0.85),
        ("EUR", "GBP", 1.15),
        ("GBP", "USD", 1.05),
        ("USD", "JPY", 145.0),
        ("JPY", "GBP", 0.0075),
    ]
    rate = {(u, v): r for u, v, r in rates}
    # прибыльный обмен по кругу становится отрицательным циклом весов -log(курс)
    edges = [(u, v, -math.log(r)) for u, v, r in rates]

    dist = {name: 0.0 for name in names}
    prev = {name: None for name in names}
    bad = None
    for _ in range(len(names)):
        bad = None
        for u, v, w in edges:
            if dist[u] + w < dist[v] - 1e-9:
                dist[v] = dist[u] + w
                prev[v] = u
                bad = v
    if bad is None:
        print("арбитражного цикла нет")
        return

    for _ in range(len(names)):
        bad = prev[bad]
    cycle = [bad]
    v = prev[bad]
    while v != bad:
        cycle.append(v)
        v = prev[v]
    cycle.append(bad)
    cycle.reverse()

    product = 1.0
    weight = 0.0
    for u, v in zip(cycle, cycle[1:]):
        product *= rate[(u, v)]
        weight -= math.log(rate[(u, v)])
    capital = 1000.0
    print("цикл: " + " -> ".join(cycle))
    print(f"вес цикла: {weight:+.4f}, цикл отрицательный")
    print(f"произведение курсов: {product:.6f}")
    print(f"капитал: {capital:.0f} -> {capital * product:.2f}, прибыль {capital * product - capital:+.2f}")


TASKS = [task_1, task_2, task_3]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TASKS[int(sys.argv[1]) - 1]()
    else:
        for task in TASKS:
            task()
            print()
