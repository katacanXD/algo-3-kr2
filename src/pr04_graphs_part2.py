import random
from collections import deque


# --- Задание 1: Краскал и Прим ---
def task1_mst():
    print("=" * 60)
    print("Задание 1. MST (Краскал и Прим)")
    vertices = ["A", "B", "C", "D", "E", "F"]
    edges = [
        ("A", "B", 4), ("A", "C", 7), ("A", "D", 3),
        ("B", "C", 5), ("B", "D", 2), ("B", "E", 6),
        ("C", "D", 5), ("D", "E", 2), ("D", "F", 1), ("E", "F", 9),
    ]

    # Алгоритм Краскала с простым DSU
    parent = {v: v for v in vertices}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    sorted_edges = sorted(edges, key=lambda x: x[2])
    kruskal_mst = []
    kruskal_weight = 0
    print("Краскал (по шагам):")
    for u, v, w in sorted_edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            kruskal_mst.append((u, v, w))
            kruskal_weight += w
            print(f"  + ({u}, {v}, {w}) — объединяем компоненты")
        else:
            print(f"  - ({u}, {v}, {w}) — образует цикл, пропускаем")
        if len(kruskal_mst) == len(vertices) - 1:
            break
    print(f"Итог Краскала: рёбра={kruskal_mst}, вес={kruskal_weight}")

    # Алгоритм Прима от вершины A
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    visited = {"A"}
    prim_mst = []
    prim_weight = 0
    print("Прим от A (по шагам):")
    while len(visited) < len(vertices):
        candidates = []
        for u in sorted(visited):
            for v, w in adj[u]:
                if v not in visited:
                    candidates.append((w, u, v))
        w, u, v = min(candidates)
        visited.add(v)
        prim_mst.append((u, v, w))
        prim_weight += w
        print(f"  + ({u}, {v}, {w}), в дереве: {sorted(visited)}")
    print(f"Итог Прима: рёбра={prim_mst}, вес={prim_weight}")


# --- Задание 2: Жадное независимое множество (деградация графа) ---
def task2_independent_set():
    print("=" * 60)
    print("Задание 2. Приближённое максимальное независимое множество")
    graph = {
        "A": {"B", "C", "D"},
        "B": {"A", "D", "E"},
        "C": {"A", "D", "E"},
        "D": {"A", "B", "C", "E"},
        "E": {"B", "C", "D", "F"},
        "F": {"E"},
    }
    remaining = {v: set(nb) for v, nb in graph.items()}
    indep_set = []
    step = 0
    while remaining:
        step += 1
        degs = {v: len(nb) for v, nb in sorted(remaining.items())}
        chosen = min(degs, key=lambda v: (degs[v], v))
        indep_set.append(chosen)
        to_remove = {chosen} | remaining[chosen]
        print(f"Шаг {step}: степени={degs} -> выбираем {chosen}, удаляем {sorted(to_remove)}")
        for v in to_remove:
            remaining.pop(v, None)
        for v in remaining:
            remaining[v] -= to_remove
    print(f"Независимое множество: {indep_set}, размер = {len(indep_set)}")


# --- Задание 3: Алгоритм Вельша-Пауэлла ---
def task3_welsh_powell():
    print("=" * 60)
    print("Задание 3. Раскраска методом Вельша-Пауэлла")
    graph = {
        "A": {"B", "C", "D"},
        "B": {"A", "D", "E"},
        "C": {"A", "D", "E"},
        "D": {"A", "B", "C", "E"},
        "E": {"B", "C", "D", "F"},
        "F": {"E"},
    }
    order = sorted(graph.keys(), key=lambda v: (-len(graph[v]), v))
    print("Сортировка по убыванию степеней:", [(v, len(graph[v])) for v in order])

    colors = {}
    buckets = []
    color_num = 0
    for v in order:
        if v in colors:
            continue
        color_num += 1
        bucket = [v]
        colors[v] = color_num
        for u in order:
            if u not in colors and all(u not in graph[b] for b in bucket):
                colors[u] = color_num
                bucket.append(u)
        buckets.append((color_num, bucket))
        print(f"  Цвет {color_num} (букет): {bucket}")
    print(f"Хроматическое число chi(G) = {len(buckets)} (в графе есть треугольник A-B-D)")


# --- Задание 4: Знаковый граф ---
def task4_signed_graph():
    print("=" * 60)
    print("Задание 4. Балансность знакового графа")
    nodes = [1, 2, 3, 4, 5]
    edges = [
        (1, 2, "+"), (1, 3, "-"), (2, 3, "-"),
        (2, 4, "+"), (3, 4, "-"), (4, 5, "-"), (1, 5, "-")
    ]
    # Пробуем разбить на 2 коалиции (0 и 1): '+' -> одинаковая группа, '-' -> разные
    adj = {v: [] for v in nodes}
    for u, v, s in edges:
        adj[u].append((v, s))
        adj[v].append((u, s))

    group = {1: 0}
    q = deque([1])
    balanced = True
    while q:
        u = q.popleft()
        for v, s in adj[u]:
            expected = group[u] if s == "+" else 1 - group[u]
            if v not in group:
                group[v] = expected
                q.append(v)
            elif group[v] != expected:
                balanced = False

    c0 = [v for v in nodes if group[v] == 0]
    c1 = [v for v in nodes if group[v] == 1]
    print(f"Граф сбалансирован: {balanced}")
    print(f"Коалиция 1: {c0}, Коалиция 2: {c1}")


# --- Задание 5: Модель Уоттса-Строгатца ---
def task5_watts_strogatz():
    print("=" * 60)
    print("Задание 5. Модель Уоттса-Строгатца (N=8, k=2)")

    def bfs_diameter(adj):
        diam = 0
        total_dist = 0
        pairs = 0
        for s in adj:
            dist = {s: 0}
            q = deque([s])
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        q.append(v)
            diam = max(diam, max(dist.values()))
            total_dist += sum(dist.values())
            pairs += len(adj) - 1
        return diam, total_dist / pairs

    # Кольцо из 8 вершин
    ring = {i: {(i - 1) % 8, (i + 1) % 8} for i in range(8)}
    d0, avg0 = bfs_diameter(ring)
    print(f"Начальное кольцо: диаметр = {d0}, среднее расстояние = {avg0:.2f}")

    # Перенаправим 2 ребра: (0,1)->(0,4) и (1,2)->(1,4)
    rewired = {i: set(nb) for i, nb in ring.items()}
    rewired[0].remove(1); rewired[1].remove(0)
    rewired[0].add(4); rewired[4].add(0)
    rewired[1].remove(2); rewired[2].remove(1)
    rewired[1].add(4); rewired[4].add(1)
    d1, avg1 = bfs_diameter(rewired)
    print(f"После перенаправления (0,1)->(0,4) и (1,2)->(1,4): диаметр = {d1}, среднее расстояние = {avg1:.2f}")


# --- Повышенная трудность 1: Симулятор Барабаши-Альберт ---
def adv1_barabasi_albert():
    print("=" * 60)
    print("Повышенная трудность 1. Модель Барабаши-Альберт (m0=3, N=1000, m=2)")
    random.seed(42)
    m0 = 3
    n_new = 1000
    m = 2

    # Начальный полный граф из 3 узлов
    adj = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    # Список вершин с повторениями пропорционально степени для простого выбора
    targets = [0, 0, 1, 1, 2, 2]

    for new_node in range(m0, m0 + n_new):
        chosen = set()
        while len(chosen) < m:
            chosen.add(random.choice(targets))
        adj[new_node] = list(chosen)
        for v in chosen:
            adj[v].append(new_node)
            targets.append(v)
            targets.append(new_node)

    degrees = [(v, len(nb)) for v, nb in adj.items()]
    top5 = sorted(degrees, key=lambda x: -x[1])[:5]
    print(f"Всего узлов: {len(adj)}, всего рёбер: {sum(len(nb) for nb in adj.values()) // 2}")
    print("Топ-5 хабов (узел, степень):", top5)


# --- Повышенная трудность 2: Раскраска регистров через МИМ ---
def adv2_register_allocation():
    print("=" * 60)
    print("Повышенная трудность 2. Распределение регистров памяти")
    graph = {
        "x1": {"x2", "x3", "x4"},
        "x2": {"x1", "x3", "x5"},
        "x3": {"x1", "x2", "x6"},
        "x4": {"x1", "x5", "x6"},
        "x5": {"x2", "x4", "x6"},
        "x6": {"x3", "x4", "x5"},
    }
    nodes = sorted(graph.keys())

    # Находим все максимальные независимые множества простым перебором
    max_indep_sets = []

    def is_indep(s):
        lst = list(s)
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                if lst[j] in graph[lst[i]]:
                    return False
        return True

    all_indep = []
    for mask in range(1, 1 << len(nodes)):
        subset = {nodes[i] for i in range(len(nodes)) if mask & (1 << i)}
        if is_indep(subset):
            all_indep.append(subset)

    for s in all_indep:
        if not any(s < other for other in all_indep):
            max_indep_sets.append(sorted(s))

    print("Все максимальные независимые множества (МИМ):")
    for mis in max_indep_sets:
        print(" ", mis)

    # Находим минимальное разбиение вершин на независимые множества
    # (каждое независимое множество — один физический регистр)
    all_nodes_set = set(nodes)
    best_coloring = None

    def solve(uncovered, used_sets):
        nonlocal best_coloring
        if best_coloring is not None and len(used_sets) >= len(best_coloring):
            return
        if not uncovered:
            best_coloring = list(used_sets)
            return
        first = min(uncovered)
        for mis in max_indep_sets:
            if first in mis:
                sub = set(mis) & uncovered
                solve(uncovered - sub, used_sets + [sorted(sub)])

    solve(all_nodes_set, [])
    print(f"Минимальное число регистров: {len(best_coloring)}")
    for idx, reg_vars in enumerate(best_coloring, 1):
        print(f"  Регистр R{idx}: {reg_vars}")


if __name__ == "__main__":
    task1_mst()
    task2_independent_set()
    task3_welsh_powell()
    task4_signed_graph()
    task5_watts_strogatz()
    adv1_barabasi_albert()
    adv2_register_allocation()
