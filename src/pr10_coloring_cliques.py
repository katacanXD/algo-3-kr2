def greedy_coloring(graph, order):
    """Простая жадная раскраска графа в заданном порядке вершин."""
    colors = {}
    for v in order:
        used = {colors[nb] for nb in graph[v] if nb in colors}
        c = 1
        while c in used:
            c += 1
        colors[v] = c
    return colors


def welsh_powell(graph):
    """Раскраска методом Вельша-Пауэлла (сортировка по убыванию степени, букеты)."""
    order = sorted(graph.keys(), key=lambda v: (-len(graph[v]), v))
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
    return colors, buckets, order


def exact_chromatic_number(graph):
    """Точное определение хроматического числа перебором для небольшого графа."""
    nodes = list(graph.keys())

    def can_color(k):
        col = {}

        def dfs(idx):
            if idx == len(nodes):
                return True
            v = nodes[idx]
            used = {col[nb] for nb in graph[v] if nb in col}
            for c in range(1, k + 1):
                if c not in used:
                    col[v] = c
                    if dfs(idx + 1):
                        return True
                    del col[v]
            return False

        return dfs(0), col

    for k in range(1, len(nodes) + 1):
        ok, col = can_color(k)
        if ok:
            return k, col
    return len(nodes), {}


def bron_kerbosch(R, P, X, graph, cliques):
    """Алгоритм Брона-Кербоша для поиска всех максимальных клик."""
    if not P and not X:
        cliques.append(sorted(R))
        return
    for v in list(P):
        bron_kerbosch(R | {v}, P & set(graph[v]), X & set(graph[v]), graph, cliques)
        P.remove(v)
        X.add(v)


# --- Задание 1: Раскраска графа ---
def task1_coloring():
    print("=" * 60)
    print("Задание 1. Раскраска графа (8 вершин)")
    graph = {
        "A": ["B", "C", "D", "E"],
        "B": ["A", "C", "F"],
        "C": ["A", "B", "D", "F", "G"],
        "D": ["A", "C", "E", "G"],
        "E": ["A", "D", "H"],
        "F": ["B", "C", "G", "H"],
        "G": ["C", "D", "F", "H"],
        "H": ["E", "F", "G"],
    }
    alpha_order = ["A", "B", "C", "D", "E", "F", "G", "H"]
    c_greedy = greedy_coloring(graph, alpha_order)
    print(f"Простой жадный ({alpha_order}):")
    print(f"  Раскраска: {c_greedy}, цветов = {max(c_greedy.values())}")

    c_wp, buckets, wp_order = welsh_powell(graph)
    print(f"Вельш-Пауэлл (порядок {wp_order}):")
    for col, b in buckets:
        print(f"  Цвет {col}: {b}")
    print(f"  Использовано цветов = {len(buckets)}")

    chi, opt_col = exact_chromatic_number(graph)
    print(f"Точное хроматическое число chi(G) = {chi} (пример раскраски: {opt_col})")


# --- Задание 2: Клики и независимые множества ---
def task2_cliques_and_indep():
    print("=" * 60)
    print("Задание 2. Клики и независимые множества (Брон-Кербош)")
    graph = {
        "A": ["B", "C", "D"],
        "B": ["A", "C", "D"],
        "C": ["A", "B", "D", "E"],
        "D": ["A", "B", "C", "F"],
        "E": ["C", "F", "G"],
        "F": ["D", "E", "G", "H"],
        "G": ["E", "F", "H"],
        "H": ["F", "G"],
    }
    cliques = []
    bron_kerbosch(set(), set(graph.keys()), set(), graph, cliques)
    cliques.sort(key=lambda c: (-len(c), c))
    print(f"Максимальные клики G ({len(cliques)}):")
    for c in cliques:
        print(f"  {c} (размер {len(c)})")
    max_clique_size = len(cliques[0])
    print(f"Наибольшая клика: {cliques[0]}, оценка снизу chi(G) >= {max_clique_size}")

    # Дополнение графа G'
    nodes = sorted(graph.keys())
    comp = {v: [u for u in nodes if u != v and u not in graph[v]] for v in nodes}
    print("Дополнение графа (списки смежности):")
    for v in nodes:
        print(f"  {v}: {comp[v]}")

    indep_sets = []
    bron_kerbosch(set(), set(comp.keys()), set(), comp, indep_sets)
    indep_sets.sort(key=lambda c: (-len(c), c))
    print(f"Максимальные независимые множества G ({len(indep_sets)}):")
    for s in indep_sets:
        print(f"  {s} (размер {len(s)})")


# --- Задание 3: Составление расписания ---
def task3_schedule():
    print("=" * 60)
    print("Задание 3. Составление расписания для 6 занятий")
    conflicts = {
        "M1": ["M2", "M3", "P1"],
        "M2": ["M1", "M3", "P2"],
        "M3": ["M1", "M2", "P1", "P2", "P3"],
        "P1": ["M1", "M3", "P2", "P3"],
        "P2": ["M2", "M3", "P1", "P3"],
        "P3": ["M3", "P1", "P2"],
    }
    colors, buckets, order = welsh_powell(conflicts)
    chi, _ = exact_chromatic_number(conflicts)
    print("Порядок по убыванию конфликтов:", [(v, len(conflicts[v])) for v in order])
    print(f"Хроматическое число (минимум слотов) = {chi}")
    for slot, group in buckets:
        print(f"  Слот {slot}: {group}")

    # Проверка корректности расписания
    valid = all(colors[u] != colors[v] for u in conflicts for v in conflicts[u])
    all_assigned = set(colors.keys()) == set(conflicts.keys())
    print(f"Проверка: конфликтов нет = {valid}, все занятия распределены = {all_assigned}")


if __name__ == "__main__":
    task1_coloring()
    task2_cliques_and_indep()
    task3_schedule()
