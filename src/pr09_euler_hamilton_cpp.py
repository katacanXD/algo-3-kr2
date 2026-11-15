from collections import deque


def fleury(graph, start=None):
    """Алгоритм Флёри для эйлерова цикла или пути (поддерживает мультиграфы)."""
    g = {v: list(nb) for v, nb in graph.items()}
    odd = [v for v in g if len(g[v]) % 2 != 0]
    if len(odd) not in (0, 2):
        return None

    def is_bridge(u, v):
        g[u].remove(v)
        g[v].remove(u)
        visited = {u}
        q = deque([u])
        while q:
            x = q.popleft()
            for y in g[x]:
                if y not in visited:
                    visited.add(y)
                    q.append(y)
        g[u].append(v)
        g[v].append(u)
        return v not in visited

    if start is None:
        start = odd[0] if odd else next(iter(g))
    circuit = [start]
    cur = start

    while any(g.values()):
        nbs = g[cur]
        nxt = None
        for nb in nbs:
            if not is_bridge(cur, nb):
                nxt = nb
                break
        if nxt is None:
            nxt = nbs[0]
        g[cur].remove(nxt)
        g[nxt].remove(cur)
        cur = nxt
        circuit.append(cur)
    return circuit


# --- Задание 1: Проверка эйлеровости ---
def task1_euler_check():
    print("=" * 60)
    print("Задание 1. Проверка эйлеровости графа (7 вершин)")
    graph = {
        "A": ["B", "C", "D"],
        "B": ["A", "C", "E"],
        "C": ["A", "B", "D", "E", "F"],
        "D": ["A", "C", "F"],
        "E": ["B", "C", "F", "G"],
        "F": ["C", "D", "E", "G"],
        "G": ["E", "F"],
    }
    degs = {v: len(nb) for v, nb in graph.items()}
    odd = [v for v, d in degs.items() if d % 2 != 0]
    print("Степени вершин:", degs)
    print(f"Нечётные вершины ({len(odd)}): {odd}")
    res = fleury(graph)
    if res is None:
        print("Вывод: граф НЕ эйлеров и НЕ полуэйлеров (нечётных вершин 4, а нужно 0 или 2).")


# --- Задание 2: Задача китайского почтальона (CPP) ---
def task2_cpp():
    print("=" * 60)
    print("Задание 2. Задача китайского почтальона (7 вершин)")
    edges = [
        ("A", "B", 6), ("A", "C", 3), ("A", "D", 8),
        ("B", "D", 5), ("B", "E", 4),
        ("C", "D", 2), ("C", "F", 7),
        ("D", "E", 3), ("D", "F", 6),
        ("E", "F", 4), ("E", "G", 5),
        ("F", "G", 2),
    ]
    nodes = ["A", "B", "C", "D", "E", "F", "G"]
    adj = {v: [] for v in nodes}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    odd = [v for v in nodes if len(adj[v]) % 2 != 0]
    print("Нечётные вершины:", odd)

    # Флойд-Уоршелл для кратчайших расстояний и восстановления путей
    INF = float("inf")
    idx = {v: i for i, v in enumerate(nodes)}
    n = len(nodes)
    dist = [[INF] * n for _ in range(n)]
    nxt = [[None] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        iu, iv = idx[u], idx[v]
        dist[iu][iv] = dist[iv][iu] = w
        nxt[iu][iv] = iv
        nxt[iv][iu] = iu

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]

    def get_path(u, v):
        iu, iv = idx[u], idx[v]
        path = [u]
        while iu != iv:
            iu = nxt[iu][iv]
            path.append(nodes[iu])
        return path

    print("Кратчайшие расстояния между нечётными вершинами:")
    for i in range(len(odd)):
        for j in range(i + 1, len(odd)):
            u, v = odd[i], odd[j]
            print(f"  {u} — {v}: {dist[idx[u]][idx[v]]} (путь {' -> '.join(get_path(u, v))})")

    # Три варианта паросочетания для 4 нечётных вершин
    a, b, c, d = odd
    matchings = [
        [(a, b), (c, d)],
        [(a, c), (b, d)],
        [(a, d), (b, c)],
    ]
    best_m = None
    best_add = INF
    for m in matchings:
        cost = sum(dist[idx[u]][idx[v]] for u, v in m)
        print(f"  Паросочетание {m}: доп. длина = {cost}")
        if cost < best_add:
            best_add = cost
            best_m = m

    print(f"Выбрано минимальное паросочетание: {best_m} (доп. длина = {best_add})")

    # Строим эйлеров мультиграф, дублируя рёбра кратчайших путей
    multi = {v: [] for v in nodes}
    weight_map = {}
    base_sum = 0
    for u, v, w in edges:
        multi[u].append(v)
        multi[v].append(u)
        weight_map[(u, v)] = weight_map[(v, u)] = w
        base_sum += w

    for u, v in best_m:
        p = get_path(u, v)
        for i in range(len(p) - 1):
            x, y = p[i], p[i + 1]
            multi[x].append(y)
            multi[y].append(x)

    circuit = fleury(multi, start="A")
    route_len = sum(weight_map[(circuit[i], circuit[i + 1])] for i in range(len(circuit) - 1))
    print("Эйлеров маршрут почтальона:", " -> ".join(circuit))
    print(f"Сумма исходных рёбер: {base_sum}, дублированные пути: {best_add}, итоговая длина: {route_len}")


# --- Задание 3: Гамильтонов цикл ---
def task3_hamiltonian():
    print("=" * 60)
    print("Задание 3. Поиск гамильтонова цикла (6 вершин)")
    graph = {
        "A": ["B", "C", "F"],
        "B": ["A", "C", "D"],
        "C": ["A", "B", "D", "E"],
        "D": ["B", "C", "E", "F"],
        "E": ["C", "D", "F"],
        "F": ["A", "D", "E"],
    }
    n = len(graph)
    degs = {v: len(nb) for v, nb in graph.items()}
    dirac_ok = all(d >= n / 2 for d in degs.values())
    print("Степени вершин:", degs)
    print(f"Теорема Дирака (deg(v) >= {n/2:.0f} для всех v): {dirac_ok}")

    def find_hamiltonian(start):
        def backtrack(path):
            if len(path) == n:
                if path[0] in graph[path[-1]]:
                    return path + [path[0]]
                return None
            for nb in graph[path[-1]]:
                if nb not in path:
                    res = backtrack(path + [nb])
                    if res:
                        return res
            return None

        return backtrack([start])

    cycle = find_hamiltonian("A")
    print("Найденный гамильтонов цикл:", " -> ".join(cycle))


if __name__ == "__main__":
    task1_euler_check()
    task2_cpp()
    task3_hamiltonian()
