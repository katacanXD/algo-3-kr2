import sys


def greedy_coloring(graph, order):
    colors = {}
    for v in order:
        used = {colors[nb] for nb in graph[v] if nb in colors}
        color = 1
        while color in used:
            color += 1
        colors[v] = color
    return colors


# один цвет - это букет: вершина и все несмежные с ней, начинаем с самых занятых
def welsh_powell(graph):
    order = sorted(graph, key=lambda v: (-len(graph[v]), v))
    colors, buckets = {}, []
    for v in order:
        if v in colors:
            continue
        color = len(buckets) + 1
        colors[v] = color
        bucket = [v]
        for u in order:
            if u not in colors and all(u not in graph[b] for b in bucket):
                colors[u] = color
                bucket.append(u)
        buckets.append(bucket)
    return colors, buckets


def dsatur(graph):
    colors = {}
    while len(colors) < len(graph):
        v = max((u for u in graph if u not in colors),
                key=lambda u: (len({colors[nb] for nb in graph[u] if nb in colors}),
                               len(graph[u]), u))
        used = {colors[nb] for nb in graph[v] if nb in colors}
        color = 1
        while color in used:
            color += 1
        colors[v] = color
    return colors


def exact_chromatic_number(graph):
    nodes = sorted(graph, key=lambda v: -len(graph[v]))

    def paint(k):
        colors = {}

        def dfs(i):
            if i == len(nodes):
                return True
            v = nodes[i]
            used = {colors[u] for u in graph[v] if u in colors}
            for color in range(1, k + 1):
                if color not in used:
                    colors[v] = color
                    if dfs(i + 1):
                        return True
                    del colors[v]
            return False

        return dfs(0), colors

    for k in range(1, len(nodes) + 1):
        ok, colors = paint(k)
        if ok:
            return k, colors
    return len(nodes), {}


def bron_kerbosch(R, P, X, graph, cliques):
    if not P and not X:
        cliques.append(sorted(R))
        return
    for v in list(P):
        bron_kerbosch(R | {v}, P & set(graph[v]), X & set(graph[v]), graph, cliques)
        P.remove(v)
        X.add(v)


def max_cliques(graph):
    cliques = []
    bron_kerbosch(set(), set(graph), set(), graph, cliques)
    return sorted(cliques, key=lambda c: (-len(c), c))


def complement(graph):
    nodes = sorted(graph)
    return {v: [u for u in nodes if u != v and u not in graph[v]] for v in nodes}


def layout(colors):
    return " ".join(f"{v}={colors[v]}" for v in sorted(colors))


def braces(names):
    return "{" + ",".join(names) + "}"


def wrap(items, width=86):
    lines, line = [], ""
    for item in items:
        if len(line) + len(item) + 2 > width:
            lines.append(line.rstrip(", "))
            line = ""
        line += item + ", "
    if line:
        lines.append(line.rstrip(", "))
    return lines


def task_1():
    print("Задание 1. Раскраска графа из 8 вершин")
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
    order = sorted(graph)
    greedy = greedy_coloring(graph, order)
    print(f"жадный ({','.join(order)}): {layout(greedy)}, цветов {max(greedy.values())}")

    wp_colors, buckets = welsh_powell(graph)
    wp_order = sorted(graph, key=lambda v: (-len(graph[v]), v))
    print(f"Вельш-Пауэлл ({','.join(wp_order)}): {layout(wp_colors)}, цветов {len(buckets)}")
    print("  букеты: " + ", ".join(braces(sorted(b)) for b in buckets))

    dsat = dsatur(graph)
    print(f"DSatur: {layout(dsat)}, цветов {max(dsat.values())}")

    chi, _ = exact_chromatic_number(graph)
    clique = max_cliques(graph)[0]
    note = "нижняя оценка по клике слабая" if chi > len(clique) else "нижняя оценка по клике точная"
    print(f"chi(G) = {chi}, наибольшая клика {braces(clique)} размера {len(clique)}: {note}")


def task_2():
    print("Задание 2. Клики и независимые множества графа из 8 вершин")
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
    cliques = max_cliques(graph)
    print(f"максимальные клики ({len(cliques)}):")
    for c in cliques:
        print(f"  {braces(c)} размера {len(c)}")
    print(f"наибольшая клика {braces(cliques[0])}, отсюда chi(G) >= {len(cliques[0])}")

    comp = complement(graph)
    edges = [braces([u, v]) for u in sorted(comp) for v in comp[u] if u < v]
    print(f"дополнение графа, рёбер {len(edges)}:")
    for line in wrap(edges):
        print("  " + line)

    # независимые множества G - это клики дополнения
    indep = max_cliques(comp)
    print(f"независимых множеств {len(indep)}, у наибольших по {len(indep[0])} вершины:")
    for line in wrap([f"{braces(s)} ({len(s)})" for s in indep]):
        print("  " + line)

    bad = sum(1 for s in indep for u in s for v in s if u < v and v in graph[u])
    print(f"проверка: смежных пар внутри этих множеств {bad}")


def task_3():
    print("Задание 3. Расписание для шести занятий")
    conflicts = {
        "M1": ["M2", "M3", "P1"],
        "M2": ["M1", "M3", "P2"],
        "M3": ["M1", "M2", "P1", "P2", "P3"],
        "P1": ["M1", "M3", "P2", "P3"],
        "P2": ["M2", "M3", "P1", "P3"],
        "P3": ["M3", "P1", "P2"],
    }
    degrees = {v: len(nb) for v, nb in conflicts.items()}
    order = sorted(conflicts, key=lambda v: (-degrees[v], v))
    print("конфликтов у занятий: " + ", ".join(f"{v} {degrees[v]}" for v in order))

    chi, _ = exact_chromatic_number(conflicts)
    clique = max_cliques(conflicts)[0]
    print(f"chi(G) = {chi}, клика {braces(clique)} требует не меньше {len(clique)} слотов")

    colors, buckets = welsh_powell(conflicts)
    print(f"Вельш-Пауэлл, слотов {len(buckets)}:")
    for i, bucket in enumerate(buckets, 1):
        print(f"  слот {i}: {', '.join(sorted(bucket))}")

    bad = sum(1 for u in conflicts for v in conflicts[u] if u < v and colors[u] == colors[v])
    print(f"распределено занятий {len(colors)} из {len(conflicts)}, нарушений {bad}")


TASKS = [task_1, task_2, task_3]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TASKS[int(sys.argv[1]) - 1]()
    else:
        for task in TASKS:
            task()
            print()
