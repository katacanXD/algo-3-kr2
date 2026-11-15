import itertools
import random
import sys
from collections import deque


def kruskal(vertices, edges):
    parent = {v: v for v in vertices}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    tree = []
    total = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru == rv:
            print(f"  ({u},{v}) вес {w}: уже в одной компоненте, пропускаем")
            continue
        parent[ru] = rv
        tree.append((u, v, w))
        total += w
        print(f"  ({u},{v}) вес {w}: берём, осталось компонент {len(vertices) - len(tree)}")
    return tree, total


def prim(vertices, edges, start):
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    visited = {start}
    tree = []
    total = 0
    while len(visited) < len(vertices):
        w, u, v = min((w, u, v) for u in visited for v, w in adj[u] if v not in visited)
        visited.add(v)
        tree.append((u, v, w))
        total += w
        print(f"  ({u},{v}) вес {w}: вершин в дереве: {len(visited)}")
    return tree, total


def task_1():
    print("Задание 1. Минимальное остовное дерево: Краскал и Прим")
    vertices = ["A", "B", "C", "D", "E", "F"]
    edges = [("A", "B", 4), ("A", "C", 7), ("A", "D", 3), ("B", "C", 5),
             ("B", "D", 2), ("B", "E", 6), ("C", "D", 5), ("D", "E", 2),
             ("D", "F", 1), ("E", "F", 9)]
    print("Краскал:")
    tree, weight = kruskal(vertices, edges)
    print(f"  рёбра MST: {tree}")
    print(f"  вес MST: {weight}")
    print("Прим от вершины A:")
    tree_p, weight_p = prim(vertices, edges, "A")
    print(f"  рёбра MST: {tree_p}")
    print(f"  вес MST: {weight_p}, совпадает с Краскалом: {weight == weight_p}")


def is_independent(graph, subset):
    return all(b not in graph[a] for a, b in itertools.combinations(subset, 2))


def format_degrees(degrees):
    return ", ".join(f"{v} {d}" for v, d in degrees.items())


def task_2():
    print("Задание 2. Жадное независимое множество вершин")
    graph = {
        "A": {"B", "C", "D"}, "B": {"A", "D", "E"}, "C": {"A", "D", "E"},
        "D": {"A", "B", "C", "E"}, "E": {"B", "C", "D", "F"}, "F": {"E"},
    }
    # вершины, которые ещё не выброшены из графа деградацией
    left = {v: set(nb) for v, nb in graph.items()}
    chosen = []
    step = 0
    while left:
        step += 1
        degrees = {v: len(left[v]) for v in sorted(left)}
        print(f"  шаг {step}, степени: {format_degrees(degrees)}")
        v = min(degrees, key=lambda x: (degrees[x], x))
        removed = {v} | left[v]
        chosen.append(v)
        print(f"  берём {v} (степень {degrees[v]}), удаляем {', '.join(sorted(removed))}")
        for u in removed:
            left.pop(u, None)
        for u in left:
            left[u] -= removed
    print(f"  множество: {', '.join(chosen)}, размер {len(chosen)}")
    best = max(len(s) for r in range(len(graph), 0, -1)
               for s in itertools.combinations(sorted(graph), r) if is_independent(graph, s))
    print(f"  проверка полным перебором: максимум {best}")


def task_3():
    print("Задание 3. Раскраска графа по Вельшу-Пауэллу")
    graph = {
        "A": {"B", "C", "D"}, "B": {"A", "D", "E"}, "C": {"A", "D", "E"},
        "D": {"A", "B", "C", "E"}, "E": {"B", "C", "D", "F"}, "F": {"E"},
    }
    order = sorted(graph, key=lambda v: (-len(graph[v]), v))
    print("  порядок: " + ", ".join(f"{v}({len(graph[v])})" for v in order))
    color = {}
    count = 0
    for v in order:
        if v in color:
            continue
        count += 1
        bucket = [v]
        color[v] = count
        skipped = []
        for u in order:
            if u in color:
                continue
            if any(u in graph[b] for b in bucket):
                skipped.append(u)
            else:
                color[u] = count
                bucket.append(u)
        print(f"  цвет {count}: {', '.join(bucket)} (пропущены: {', '.join(skipped) or '-'})")
    triangle = next(t for t in itertools.combinations(sorted(graph), 3)
                    if all(b in graph[a] for a, b in itertools.combinations(t, 2)))
    print(f"  χ(G) = {count}; треугольник {'-'.join(triangle)} даёт оценку снизу 3")


def tree_path(node, parent):
    path = []
    while node is not None:
        path.append(node)
        node = parent[node]
    return path


def unbalanced_cycle(edge, parent):
    left, right = tree_path(edge[0], parent), tree_path(edge[1], parent)
    common = next(x for x in left if x in right)
    return left[:left.index(common) + 1] + right[:right.index(common)][::-1]


def task_4():
    print("Задание 4. Структурный баланс знаковой социальной сети")
    edges = [(1, 2, "+"), (1, 3, "-"), (2, 3, "-"), (2, 4, "+"), (3, 4, "-"),
             (4, 5, "-"), (1, 5, "-")]
    adj = {}
    for u, v, sign in edges:
        adj.setdefault(u, []).append((v, sign))
        adj.setdefault(v, []).append((u, sign))
    side = {1: 0}
    parent = {1: None}
    queue = deque([1])
    clash = None
    while queue:
        u = queue.popleft()
        for v, sign in adj[u]:
            want = side[u] if sign == "+" else 1 - side[u]
            if v not in side:
                side[v] = want
                parent[v] = u
                queue.append(v)
            elif side[v] != want and clash is None:
                clash = (u, v)
    if clash is None:
        print("  все рёбра согласованы, граф структурно сбалансирован")
        for s in (0, 1):
            coalition = [str(v) for v in sorted(side) if side[v] == s]
            print(f"  коалиция {s + 1}: {', '.join(coalition)}")
    else:
        cycle = unbalanced_cycle(clash, parent)
        print(f"  граф не сбалансирован, цикл: {'-'.join(map(str, cycle))}-{cycle[0]}")


def graph_stats(adj):
    matrix = {}
    for start in adj:
        dist = {start: 0}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        matrix[start] = dist
    diameter = max(max(d.values()) for d in matrix.values())
    average = sum(sum(d.values()) for d in matrix.values()) / (len(adj) * (len(adj) - 1))
    return diameter, average, matrix


def task_5():
    print("Задание 5. Модель малого мира Уоттса-Строгатца (N=8, k=2)")
    n = 8
    ring = {i: {(i - 1) % n, (i + 1) % n} for i in range(n)}
    d0, a0, before = graph_stats(ring)
    print(f"  кольцо: диаметр {d0}, среднее расстояние {a0:.2f}")
    rewired = {i: set(nb) for i, nb in ring.items()}
    # ребро (u,v) переезжает на (u,z), где z лежит на другом конце кольца
    for u, v, z in [(0, 1, 4), (1, 2, 4)]:
        rewired[u].discard(v)
        rewired[v].discard(u)
        rewired[u].add(z)
        rewired[z].add(u)
    print("  перенаправили (0,1) на (0,4), (1,2) на (1,4)")
    d1, a1, after = graph_stats(rewired)
    print(f"  после rewiring: диаметр {d1}, среднее расстояние {a1:.2f}")
    for x, y in [(0, 4), (1, 5), (2, 7)]:
        print(f"  расстояние {x}-{y}: было {before[x][y]}, стало {after[x][y]}")


def task_6():
    print("Повышенная трудность 1. Сеть Барабаши-Альберта (m0=3, N=1000, m=2)")
    random.seed(42)
    m0, n_new, m = 3, 1000, 2
    adj = {v: set() for v in range(m0)}
    for u in range(m0):
        for v in range(u + 1, m0):
            adj[u].add(v)
            adj[v].add(u)
    # узел попадает в список столько раз, какова его степень
    repeated = [v for v in adj for _ in range(len(adj[v]))]
    for new in range(m0, m0 + n_new):
        chosen = set()
        while len(chosen) < m:
            chosen.add(random.choice(repeated))
        adj[new] = set(chosen)
        for v in chosen:
            adj[v].add(new)
            repeated.extend([v, new])
    top = sorted(adj, key=lambda v: (-len(adj[v]), v))[:5]
    edge_count = sum(len(nb) for nb in adj.values()) // 2
    print(f"  узлов {len(adj)}, рёбер {edge_count}, средняя степень "
          f"{2 * edge_count / len(adj):.2f}")
    print("  топ-5 хабов: " + ", ".join(f"{v} (степень {len(adj[v])})" for v in top))


def task_7():
    print("Повышенная трудность 2. Раскраска регистров памяти")
    graph = {
        "x1": {"x2", "x3", "x4"}, "x2": {"x1", "x3", "x5"}, "x3": {"x1", "x2", "x6"},
        "x4": {"x1", "x5", "x6"}, "x5": {"x2", "x4", "x6"}, "x6": {"x3", "x4", "x5"},
    }
    nodes = sorted(graph)
    independent_sets = [s for r in range(1, len(nodes) + 1)
                        for s in itertools.combinations(nodes, r) if is_independent(graph, s)]
    maximal = [s for s in independent_sets
               if not any(set(s) < set(t) for t in independent_sets)]
    print("  максимальные независимые множества: " + "; ".join(", ".join(s) for s in maximal))
    best = None

    def cover(left, used):
        nonlocal best
        if best is not None and len(used) >= len(best):
            return
        if not left:
            best = list(used)
            return
        first = min(left)
        for s in maximal:
            if first in s:
                cover(left - set(s), used + [s])

    cover(set(nodes), [])
    lower = -(-len(nodes) // max(len(s) for s in maximal))
    print(f"  минимум регистров: {len(best)} (оценка снизу {lower})")
    for i, s in enumerate(best, 1):
        print(f"  R{i}: {', '.join(sorted(s))}")


TASKS = [task_1, task_2, task_3, task_4, task_5, task_6, task_7]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TASKS[int(sys.argv[1]) - 1]()
    else:
        for task in TASKS:
            task()
            print()
