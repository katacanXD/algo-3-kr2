from collections import deque


def max_flow(vertices, edges, source, sink, use_bfs=False, title=""):
    """
    Простая реализация алгоритма Форда-Фалкерсона (DFS)
    и Эдмондса-Карпа (BFS при use_bfs=True).
    """
    print("=" * 60)
    if title:
        print(title)
    print(f"Исток: {source}, Сток: {sink}")

    # Строим остаточную сеть: residual[u][v] = остаточная пропускная способность
    residual = {v: {} for v in vertices}
    for u, v, cap in edges:
        residual[u][v] = residual[u].get(v, 0) + cap
        residual[v].setdefault(u, 0)

    def find_path():
        parent = {source: None}
        if use_bfs:
            # Поиск в ширину (Эдмондс-Карп)
            q = deque([source])
            while q:
                u = q.popleft()
                if u == sink:
                    break
                for v, cap in residual[u].items():
                    if v not in parent and cap > 0:
                        parent[v] = u
                        q.append(v)
        else:
            # Поиск в глубину (Форд-Фалкерсон)
            stack = [source]
            while stack:
                u = stack.pop()
                if u == sink:
                    break
                for v, cap in residual[u].items():
                    if v not in parent and cap > 0:
                        parent[v] = u
                        stack.append(v)

        if sink not in parent:
            return None, 0

        # Восстанавливаем путь и находим минимальную пропускную способность
        path = []
        v = sink
        bottleneck = float("inf")
        while v != source:
            u = parent[v]
            path.append(v)
            bottleneck = min(bottleneck, residual[u][v])
            v = u
        path.append(source)
        path.reverse()
        return path, bottleneck

    total_flow = 0
    step = 0

    while True:
        path, flow = find_path()
        if path is None:
            break
        step += 1
        total_flow += flow

        # Обновляем остаточную сеть
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            residual[u][v] -= flow
            residual[v][u] += flow

        print(f"Шаг {step}: путь {' -> '.join(map(str, path))}, поток = {flow}, суммарно = {total_flow}")
        if use_bfs:
            active = []
            for u in vertices:
                for v, c in residual[u].items():
                    if c > 0:
                        active.append(f"{u}->{v}:{c}")
            print("  Остаточная сеть:", ", ".join(active))

    print(f"Итоговый максимальный поток: {total_flow} (итераций: {step})")
    print("Потоки по рёбрам:")
    for u, v, cap in edges:
        used = cap - residual[u][v]
        # Учитываем случай, если есть несколько дуг или обратный поток
        used = max(0, min(cap, used))
        print(f"  {u} -> {v}: {used}/{cap}")

    # Минимальный разрез: вершины, достижимые из истока в остаточной сети
    reachable = {source}
    q = deque([source])
    while q:
        u = q.popleft()
        for v, cap in residual[u].items():
            if cap > 0 and v not in reachable:
                reachable.add(v)
                q.append(v)
    cut_edges = [(u, v, cap) for u, v, cap in edges if u in reachable and v not in reachable]
    print(f"Минимальный разрез: S'={sorted(reachable, key=str)}, рёбра={[f'{u}->{v}({c})' for u,v,c in cut_edges]}")
    return total_flow


if __name__ == "__main__":
    # Задания для самостоятельного решения
    max_flow(
        ["1", "2", "3", "4", "5", "6"],
        [
            ("1", "2", 3), ("1", "4", 5), ("4", "2", 4), ("2", "3", 5),
            ("4", "5", 2), ("3", "5", 6), ("3", "6", 5), ("5", "6", 7),
        ],
        "1", "6", title="Самостоятельное задание 1 (Форд-Фалкерсон)"
    )

    max_flow(
        ["S", "A", "B", "C", "D", "E", "F", "T"],
        [
            ("S", "A", 10), ("S", "B", 5), ("A", "C", 8), ("B", "D", 6),
            ("C", "E", 6), ("C", "D", 3), ("D", "F", 5), ("E", "F", 8), ("F", "T", 10),
        ],
        "S", "T", title="Самостоятельное задание 2 (Форд-Фалкерсон)"
    )

    max_flow(
        ["S", "A", "B", "C", "D", "E", "F", "T"],
        [
            ("S", "A", 12), ("S", "B", 7), ("A", "C", 5), ("B", "C", 3),
            ("C", "E", 6), ("C", "D", 10), ("D", "E", 5), ("D", "F", 4),
            ("E", "F", 5), ("F", "T", 7),
        ],
        "S", "T", title="Самостоятельное задание 3 (Форд-Фалкерсон)"
    )

    # Задания повышенной трудности
    max_flow(
        ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        [
            ("1", "2", 28), ("5", "1", 41), ("2", "3", 23), ("2", "7", 5),
            ("3", "5", 23), ("3", "4", 19), ("3", "7", 47), ("4", "5", 46),
            ("4", "6", 12), ("5", "9", 21), ("6", "9", 17), ("7", "8", 11),
            ("8", "9", 43),
        ],
        "1", "9", title="Повышенная трудность 1 (Форд-Фалкерсон)"
    )

    max_flow(
        ["S", "A", "B", "C", "D", "E", "F", "G", "T"],
        [
            ("S", "A", 9), ("S", "B", 7), ("A", "C", 4), ("B", "D", 6),
            ("C", "E", 8), ("D", "E", 5), ("E", "F", 7), ("F", "G", 9), ("G", "T", 10),
        ],
        "S", "T", title="Повышенная трудность 2 (Форд-Фалкерсон)"
    )

    max_flow(
        ["S", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "T"],
        [
            ("S", "A", 10), ("S", "B", 15),
            ("A", "C", 10), ("A", "D", 5),
            ("B", "D", 10), ("B", "E", 10),
            ("C", "F", 10), ("D", "F", 10), ("D", "G", 5),
            ("E", "G", 10), ("E", "H", 5),
            ("F", "I", 10), ("G", "I", 10), ("G", "J", 5), ("H", "J", 10),
            ("I", "K", 15), ("I", "T", 5), ("J", "K", 10), ("J", "T", 7), ("K", "T", 10),
        ],
        "S", "T", title="Повышенная трудность 3 (Форд-Фалкерсон)"
    )

    max_flow(
        ["S", "A", "B", "C", "D", "T"],
        [
            ("S", "A", 10), ("S", "B", 5), ("A", "C", 9),
            ("B", "C", 4), ("B", "D", 8), ("C", "T", 10), ("D", "T", 10),
        ],
        "S", "T", use_bfs=True, title="Повышенная трудность 4 (Эдмондс-Карп)"
    )
