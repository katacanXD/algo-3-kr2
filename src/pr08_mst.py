import heapq
import math
import sys


def kruskal(vertices, edges):
    # DSU: parent[x] - представитель множества, find сжимает пути
    parent = {v: v for v in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    mst = []
    total = 0
    for w, u, v in sorted(edges):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            mst.append((u, v, w))
            total += w
            if len(mst) == len(vertices) - 1:
                break
    return mst, total


def prim(vertices, start, edges):
    # ленивый Прим: в кучу кладём все рёбра из добавленных вершин, старые пропускаем
    adj = {v: [] for v in vertices}
    for w, u, v in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))
    seen = {start}
    heap = [(w, start, v) for w, v in adj[start]]
    heapq.heapify(heap)
    mst = []
    total = 0
    while heap and len(seen) < len(vertices):
        w, u, v = heapq.heappop(heap)
        if v in seen:
            continue
        seen.add(v)
        mst.append((u, v, w))
        total += w
        for nw, nxt in adj[v]:
            if nxt not in seen:
                heapq.heappush(heap, (nw, v, nxt))
    return mst, total


def edge_line(mst):
    return ", ".join(f"{min(u, v)}-{max(u, v)} {w}" for u, v, w in mst)


def set_line(items):
    return "{" + ", ".join(sorted(items)) + "}"


def cut_for_edge(vertices, mst, edges, target):
    # убираем ребро из дерева, две полученные части вершин и есть нужный разрез
    tu, tv, _ = target
    tree = {v: [] for v in vertices}
    for u, v, w in mst:
        if {u, v} != {tu, tv}:
            tree[u].append(v)
            tree[v].append(u)
    part = {tu}
    stack = [tu]
    while stack:
        x = stack.pop()
        for y in tree[x]:
            if y not in part:
                part.add(y)
                stack.append(y)
    rest = set(vertices) - part
    crossing = sorted((w, u, v) for w, u, v in edges if (u in part) != (v in part))
    return part, rest, crossing


def task_1():
    print("Задание 1. Минимальное остовное дерево графа из 8 вершин")
    vertices = ["A", "B", "C", "D", "E", "F", "G", "H"]
    # на рисунке подписи рёбер B-F и D-E легли в одну точку, у D-E вес принят 4
    edges = [
        (6, "A", "B"), (4, "A", "C"), (8, "A", "D"), (2, "B", "C"), (7, "B", "E"),
        (5, "B", "F"), (3, "C", "D"), (4, "D", "E"), (5, "D", "F"), (6, "D", "G"),
        (4, "E", "F"), (3, "E", "H"), (2, "F", "G"), (8, "F", "H"), (5, "G", "H"),
    ]
    k_mst, k_total = kruskal(vertices, edges)
    p_mst, p_total = prim(vertices, "A", edges)
    print(f"Краскал: вес {k_total}, рёбер {len(k_mst)}: {edge_line(k_mst)}")
    print(f"Прим:    вес {p_total}, рёбер {len(p_mst)}: {edge_line(p_mst)}")
    print("веса совпали" if k_total == p_total else f"веса разошлись: {k_total} и {p_total}")

    target = k_mst[0]
    part, rest, crossing = cut_for_edge(vertices, k_mst, edges, target)
    w0, u0, v0 = crossing[0]
    print(f"разрез для {target[0]}-{target[1]}: S = {set_line(part)}, V\\S = {set_line(rest)}")
    print("пересекают разрез: " + edge_line([(u, v, w) for w, u, v in crossing]))
    same = {u0, v0} == {target[0], target[1]}
    print(f"минимум в разрезе {u0}-{v0} {w0}, " + ("это ребро дерева" if same else "ребро не то"))


def task_2():
    print("Задание 2. Сеть железных дорог между 11 городами")
    cities = ["SPb", "Moscow", "NNovgorod", "Kazan", "Ufa", "Ekaterinburg",
              "Tyumen", "Samara", "Volgograd", "Rostov", "Krasnodar"]
    edges = [
        (1200, "SPb", "NNovgorod"), (650, "SPb", "Moscow"), (400, "Moscow", "NNovgorod"),
        (800, "Moscow", "Kazan"), (1100, "Moscow", "Rostov"), (400, "NNovgorod", "Kazan"),
        (500, "Kazan", "Ufa"), (450, "Kazan", "Samara"), (450, "Ufa", "Samara"),
        (550, "Ufa", "Ekaterinburg"), (350, "Ekaterinburg", "Tyumen"),
        (850, "Samara", "Volgograd"), (900, "Samara", "Rostov"),
        (400, "Volgograd", "Rostov"), (250, "Rostov", "Krasnodar"),
    ]
    mst, total = kruskal(cities, edges)
    print(f"в MST {len(mst)} дорог, общая длина {total} км:")
    for u, v, w in mst:
        print(f"   {u}-{v} {w} км")

    deg = {c: 0 for c in cities}
    for u, v, _ in mst:
        deg[u] += 1
        deg[v] += 1
    for d in sorted(set(deg.values()), reverse=True):
        print(f"степень {d}: " + ", ".join(c for c in cities if deg[c] == d))
    top = max(deg.values())
    print("центральные города: " + ", ".join(c for c in cities if deg[c] == top))

    new_edges = [(500, "Moscow", "Kazan") if {u, v} == {"Moscow", "Kazan"} else (w, u, v)
                 for w, u, v in edges]
    new_total = kruskal(cities, new_edges)[1]
    print(f"с дорогой Moscow-Kazan 500 км: {new_total} км, "
          + ("дерево прежнее" if new_total == total else "дерево изменилось"))
    print("  новое ребро не нужно: между Moscow и Kazan есть путь 400 + 400 км")


def task_3():
    print("Задание 3. Электрическая сеть из 8 подстанций")
    vertices = ["1", "2", "3", "4", "5", "6", "7", "8"]
    edges = [
        (7, "1", "2"), (4, "1", "3"), (6, "1", "4"), (6, "2", "3"), (3, "2", "5"),
        (4, "2", "6"), (5, "3", "4"), (2, "3", "5"), (7, "4", "6"), (5, "4", "7"),
        (4, "5", "6"), (6, "5", "8"), (3, "6", "7"), (5, "6", "8"), (2, "7", "8"),
    ]
    k_mst, k_total = kruskal(vertices, edges)
    p_mst, p_total = prim(vertices, "1", edges)
    print(f"Краскал: стоимость {k_total}, линий {len(k_mst)}: {edge_line(k_mst)}")
    print(f"Прим:    стоимость {p_total}, линий {len(p_mst)}: {edge_line(p_mst)}")
    print("стоимости совпали" if k_total == p_total else f"стоимости разные: {k_total} и {p_total}")

    good = 0
    print("проверка леммы о безопасном ребре:")
    for edge in k_mst:
        part, rest, crossing = cut_for_edge(vertices, k_mst, edges, edge)
        safe = crossing[0][0] == edge[2]
        good += safe
        print(f"   {edge[0]}-{edge[1]} ({edge[2]}): {set_line(part)} | {set_line(rest)}, "
              f"минимум {crossing[0][0]}, " + ("да" if safe else "нет"))
    print(f"подтвердилось {good} рёбер из {len(k_mst)}")

    e, v = len(edges), len(vertices)
    print(f"сложность для E={e}, V={v}: Краскал E log E = {e * math.log2(e):.1f}, "
          f"Прим E log V = {e * math.log2(v):.1f}")
    print("на таких размерах оба быстрые, меньше сравнений у Прима")


TASKS = [task_1, task_2, task_3]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TASKS[int(sys.argv[1]) - 1]()
    else:
        for task in TASKS:
            task()
            print()
