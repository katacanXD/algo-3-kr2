import sys
from collections import Counter, deque
from math import factorial


def is_bridge(g, u, v):
    g[u].remove(v)
    g[v].remove(u)
    seen = {u}
    queue = deque([u])
    while queue:
        x = queue.popleft()
        for y in g[x]:
            if y not in seen:
                seen.add(y)
                queue.append(y)
    g[u].append(v)
    g[v].append(u)
    return v not in seen


# Флёри: из текущей вершины идём по не-мосту, мост пускаем в ход только если выбора уже нет
def fleury(graph, start):
    g = {v: list(nb) for v, nb in graph.items()}
    route = [start]
    while any(g.values()):
        cur = route[-1]
        nxt = next((nb for nb in g[cur] if not is_bridge(g, cur, nb)), g[cur][0])
        g[cur].remove(nxt)
        g[nxt].remove(cur)
        route.append(nxt)
    return route


def show_degrees(graph):
    deg = {v: len(nb) for v, nb in graph.items()}
    print("степени: " + ", ".join(f"{v}={deg[v]}" for v in graph))
    return deg


# Флойд-Уоршелл: расстояния между всеми парами вершин и первые шаги кратчайших путей
def shortest_paths(nodes, edges):
    dist = {u: {v: (0 if u == v else float("inf")) for v in nodes} for u in nodes}
    step = {}
    for u, v, w in edges:
        dist[u][v] = dist[v][u] = w
        step[u, v], step[v, u] = v, u
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    step[i, j] = step[i, k]
    return dist, step


def path_between(step, u, v):
    path = [u]
    while u != v:
        u = step[u, v]
        path.append(u)
    return path


def task_1():
    print("Задание 1. Эйлеровость графа из 7 вершин")
    graph = {
        "A": ["B", "C", "D"],
        "B": ["A", "C", "E"],
        "C": ["A", "B", "D", "E", "F"],
        "D": ["A", "C", "F"],
        "E": ["B", "C", "F", "G"],
        "F": ["C", "D", "E", "G"],
        "G": ["E", "F"],
    }
    deg = show_degrees(graph)
    odd = [v for v in graph if deg[v] % 2 != 0]
    print(f"рёбер {sum(deg.values()) // 2}, сумма степеней {sum(deg.values())}")
    print(f"нечётные вершины ({len(odd)}): " + ", ".join(odd))
    if len(odd) == 0:
        print("вывод: все степени чётные, граф эйлеров")
        print("эйлеров цикл: " + " -> ".join(fleury(graph, next(iter(graph)))))
    elif len(odd) == 2:
        print(f"вывод: граф полуэйлеров, нечётные только {odd[0]} и {odd[1]}")
        print("эйлеров путь: " + " -> ".join(fleury(graph, odd[0])))
    else:
        print(f"вывод: ни цикла, ни пути нет: нечётных {len(odd)}, а нужно 0 или 2")


def task_2():
    print("Задание 2. Задача китайского почтальона")
    edges = [
        ("A", "B", 6), ("A", "C", 3), ("A", "D", 8),
        ("B", "D", 5), ("B", "E", 4),
        ("C", "D", 2), ("C", "F", 7),
        ("D", "E", 3), ("D", "F", 6),
        ("E", "F", 4), ("E", "G", 5),
        ("F", "G", 2),
    ]
    nodes = ["A", "B", "C", "D", "E", "F", "G"]
    graph = {v: [] for v in nodes}
    weight = {}
    for u, v, w in edges:
        graph[u].append(v)
        graph[v].append(u)
        weight[u, v] = weight[v, u] = w

    deg = show_degrees(graph)
    odd = [v for v in nodes if deg[v] % 2 != 0]
    print("нечётные вершины: " + ", ".join(odd))
    dist, step = shortest_paths(nodes, edges)
    pieces = []
    for i, u in enumerate(odd):
        for v in odd[i + 1:]:
            path = path_between(step, u, v)
            tail = f" ({'-'.join(path)})" if len(path) > 2 else ""
            pieces.append(f"{u}-{v} {dist[u][v]}{tail}")
    print("кратчайшие пути: " + ", ".join(pieces))

    # нечётных вершин четыре, поэтому вариантов паросочетания всего три
    a, b, c, d = odd
    variants = [[(a, b), (c, d)], [(a, c), (b, d)], [(a, d), (b, c)]]
    costs = [sum(dist[u][v] for u, v in pairs) for pairs in variants]
    print("паросочетания: " + ", ".join(
        "+".join(f"{u}{v}" for u, v in pairs) + f"={cost}"
        for pairs, cost in zip(variants, costs)))
    best = variants[costs.index(min(costs))]

    extra = []
    for u, v in best:
        path = path_between(step, u, v)
        extra += list(zip(path, path[1:]))
    print("дублируем: " + ", ".join(f"{u}-{v} ({weight[u, v]})" for u, v in extra))

    multi = {v: list(nb) for v, nb in graph.items()}
    for u, v in extra:
        multi[u].append(v)
        multi[v].append(u)
    route = fleury(multi, "A")
    base = sum(w for _, _, w in edges)
    total = sum(weight[route[i], route[i + 1]] for i in range(len(route) - 1))
    print(f"сумма рёбер {base}, дубли {total - base}, итоговая длина {total}")
    print("маршрут Флёри: " + " -> ".join(route))

    steps = Counter(tuple(sorted(edge)) for edge in zip(route, route[1:]))
    need = Counter(tuple(sorted((u, v))) for u, v, _ in edges)
    need += Counter(tuple(sorted(edge)) for edge in extra)
    print(f"проверка: рёбер {sum(need.values())}, шагов {sum(steps.values())}, "
          f"каждое по разу: {'да' if steps == need else 'нет'}")


def task_3():
    print("Задание 3. Гамильтонов цикл в графе из 6 вершин")
    graph = {
        "A": ["B", "C", "F"],
        "B": ["A", "C", "D"],
        "C": ["A", "B", "D", "E"],
        "D": ["B", "C", "E", "F"],
        "E": ["C", "D", "F"],
        "F": ["A", "D", "E"],
    }
    deg = show_degrees(graph)
    n = len(graph)
    dirac = min(deg.values()) * 2 >= n
    print(f"условие Дирака deg(v) >= {n // 2}: {'выполнено' if dirac else 'не выполнено'}")

    calls = 0

    # перебор с возвратом: наращиваем путь, пока не обойдём все вершины и не вернёмся в старт
    def search(path):
        nonlocal calls
        calls += 1
        if len(path) == n:
            return path + [path[0]] if path[0] in graph[path[-1]] else None
        for nb in graph[path[-1]]:
            if nb not in path:
                found = search(path + [nb])
                if found:
                    return found
        return None

    cycle = search(["A"])
    if cycle is None:
        print("гамильтонов цикл не найден")
    else:
        print("гамильтонов цикл: " + " -> ".join(cycle))
    print(f"вызовов перебора {calls}, перестановок всего (n-1)! = {factorial(n - 1)}")


TASKS = [task_1, task_2, task_3]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TASKS[int(sys.argv[1]) - 1]()
    else:
        for task in TASKS:
            task()
            print()
