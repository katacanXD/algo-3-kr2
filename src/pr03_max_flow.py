import sys
from collections import deque


# остаточная сеть: res[u][v] - сколько ещё можно пропустить по ребру u->v
def make_residual(graph):
    res = {u: {} for u in graph}
    for u in graph:
        for v, cap in graph[u]:
            res[u][v] = res[u].get(v, 0) + cap
            res[v].setdefault(u, 0)
    return res


def find_path(res, source, sink, bfs):
    parent = {source: None}
    queue = deque([source]) if bfs else [source]
    while queue:
        u = queue.popleft() if bfs else queue.pop()
        if u == sink:
            break
        for v, cap in res[u].items():
            if cap > 0 and v not in parent:
                parent[v] = u
                queue.append(v)
    if sink not in parent:
        return None
    path = []
    v = sink
    while v is not None:
        path.append(v)
        v = parent[v]
    return path[::-1]


def max_flow(graph, source, sink, bfs=False):
    res = make_residual(graph)
    total = 0
    step = 0
    while True:
        path = find_path(res, source, sink, bfs)
        if path is None:
            break
        flow = min(res[path[i]][path[i + 1]] for i in range(len(path) - 1))
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            res[u][v] -= flow
            res[v][u] += flow
        total += flow
        step += 1
        print(f"шаг {step}: {' -> '.join(path)}, поток {flow}, суммарно {total}")
        if bfs:
            left = [f"{u}->{v}:{cap}" for u in res for v, cap in res[u].items() if cap > 0]
            print("   остаточная сеть: " + ", ".join(left))

    print(f"максимальный поток: {total} (итераций {step})")

    print("поток по рёбрам:")
    for u in graph:
        for v, cap in graph[u]:
            print(f"   {u} -> {v}: {cap - res[u][v]} / {cap}")

    reachable = {source}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v, cap in res[u].items():
            if cap > 0 and v not in reachable:
                reachable.add(v)
                queue.append(v)
    cut = [(u, v, cap) for u in graph for v, cap in graph[u]
           if u in reachable and v not in reachable]
    print("минимальный разрез: " + ", ".join(f"{u}->{v} ({cap})" for u, v, cap in cut))
    return total


def task_1():
    print("Задание 1. Наибольший поток из вершины 1 в вершину 6")
    graph = {
        "1": [("2", 3), ("4", 5)],
        "2": [("3", 5)],
        "3": [("5", 6), ("6", 5)],
        "4": [("2", 4), ("5", 2)],
        "5": [("6", 7)],
        "6": [],
    }
    max_flow(graph, "1", "6")


def task_2():
    print("Задание 2. Максимальный поток из S в T")
    graph = {
        "S": [("A", 10), ("B", 5)],
        "A": [("C", 8)],
        "B": [("D", 6)],
        "C": [("E", 6), ("D", 3)],
        "D": [("F", 5)],
        "E": [("F", 8)],
        "F": [("T", 10)],
        "T": [],
    }
    max_flow(graph, "S", "T")


def task_3():
    print("Задание 3. Наибольший поток из S в T")
    graph = {
        "S": [("A", 12), ("B", 7)],
        "A": [("C", 5)],
        "B": [("C", 3)],
        "C": [("E", 6), ("D", 10)],
        "D": [("E", 5), ("F", 4)],
        "E": [("F", 5)],
        "F": [("T", 7)],
        "T": [],
    }
    max_flow(graph, "S", "T")


def task_4():
    print("Повышенная трудность 1. Наибольший поток из вершины 1 в вершину 9")
    graph = {
        "1": [("2", 28)],
        "2": [("3", 23), ("7", 5)],
        "3": [("5", 23), ("4", 19), ("7", 47)],
        "4": [("5", 46), ("6", 12)],
        "5": [("1", 41), ("9", 21)],
        "6": [("9", 17)],
        "7": [("8", 11)],
        "8": [("9", 43)],
        "9": [],
    }
    max_flow(graph, "1", "9")


def task_5():
    print("Повышенная трудность 2. Максимальный поток из S в T")
    graph = {
        "S": [("A", 9), ("B", 7)],
        "A": [("C", 4)],
        "B": [("D", 6)],
        "C": [("E", 8)],
        "D": [("E", 5)],
        "E": [("F", 7)],
        "F": [("G", 9)],
        "G": [("T", 10)],
        "T": [],
    }
    max_flow(graph, "S", "T")


def task_6():
    print("Повышенная трудность 3. Максимальный поток из S в T")
    graph = {
        "S": [("A", 10), ("B", 15)],
        "A": [("C", 10), ("D", 5)],
        "B": [("D", 10), ("E", 10)],
        "C": [("F", 10)],
        "D": [("F", 10), ("G", 5)],
        "E": [("G", 10), ("H", 5)],
        "F": [("I", 10)],
        "G": [("I", 10), ("J", 5)],
        "H": [("J", 10)],
        "I": [("K", 15), ("T", 5)],
        "J": [("K", 10), ("T", 7)],
        "K": [("T", 10)],
        "T": [],
    }
    max_flow(graph, "S", "T")


def task_7():
    print("Повышенная трудность 4. Эдмондс-Карп: поток, остаточная сеть на каждом шаге")
    graph = {
        "S": [("A", 10), ("B", 5)],
        "A": [("C", 9)],
        "B": [("C", 4), ("D", 8)],
        "C": [("T", 10)],
        "D": [("T", 10)],
        "T": [],
    }
    max_flow(graph, "S", "T", bfs=True)


TASKS = [task_1, task_2, task_3, task_4, task_5, task_6, task_7]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TASKS[int(sys.argv[1]) - 1]()
    else:
        for task in TASKS:
            task()
            print()
