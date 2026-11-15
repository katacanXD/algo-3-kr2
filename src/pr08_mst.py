import heapq
import math
from collections import deque


def kruskal(vertices, edges):
    """Простой алгоритм Краскала с DSU."""
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


def prim(vertices, edges, start):
    """Простой алгоритм Прима с приоритетной очередью."""
    adj = {v: [] for v in vertices}
    for w, u, v in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))

    visited = set()
    pq = [(0, start, None)]
    mst = []
    total = 0

    while pq and len(visited) < len(vertices):
        w, u, parent = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if parent is not None:
            mst.append((parent, u, w))
            total += w
        for nw, v in adj[u]:
            if v not in visited:
                heapq.heappush(pq, (nw, v, u))
    return mst, total


def find_cut_for_edge(vertices, mst, edges, target_edge):
    """Строит разрез (S, V\\S), удалив target_edge из MST, и проверяет минимальность."""
    tu, tv, tw = target_edge
    tree_adj = {v: [] for v in vertices}
    for u, v, w in mst:
        if (u, v) != (tu, tv) and (v, u) != (tu, tv):
            tree_adj[u].append(v)
            tree_adj[v].append(u)

    # Обходим одну компоненту из tu
    part_s = {tu}
    q = deque([tu])
    while q:
        cur = q.popleft()
        for nb in tree_adj[cur]:
            if nb not in part_s:
                part_s.add(nb)
                q.append(nb)
    part_t = set(vertices) - part_s

    crossing = [(u, v, w) for w, u, v in edges if (u in part_s and v in part_t) or (v in part_s and u in part_t)]
    min_w = min(w for _, _, w in crossing)
    return sorted(part_s), sorted(part_t), crossing, tw == min_w


# --- Задание 1: MST двумя способами ---
def task1_mst_two_ways():
    print("=" * 60)
    print("Задание 1. MST алгоритмами Краскала и Прима (8 вершин, 15 рёбер)")
    vertices = ["A", "B", "C", "D", "E", "F", "G", "H"]
    # Примечание: на рисунке подпись ребра D-E перекрывается с пересекающим ребром B-F (5);
    # для определённости принято w(D, E) = 4.
    edges = [
        (6, "A", "B"), (4, "A", "C"), (8, "A", "D"),
        (2, "B", "C"), (7, "B", "E"), (5, "B", "F"),
        (3, "C", "D"), (4, "D", "E"), (5, "D", "F"), (6, "D", "G"),
        (4, "E", "F"), (3, "E", "H"), (2, "F", "G"), (8, "F", "H"), (5, "G", "H"),
    ]

    k_mst, k_tot = kruskal(vertices, edges)
    p_mst, p_tot = prim(vertices, edges, "A")
    print(f"Краскал (вес = {k_tot}): {k_mst}")
    print(f"Прим    (вес = {p_tot}): {p_mst}")

    part_s, part_t, crossing, ok = find_cut_for_edge(vertices, k_mst, edges, k_mst[0])
    print(f"Разрез для ребра {k_mst[0]}: S={part_s}, V\\S={part_t}")
    print(f"  Пересекающие рёбра: {crossing}, минимальность подтверждена: {ok}")


# --- Задание 2: Сеть железных дорог между 11 городами ---
def task2_railways():
    print("=" * 60)
    print("Задание 2. Железнодорожная сеть (11 городов)")
    cities = [
        "SPb", "Moscow", "NNovgorod", "Kazan", "Ufa",
        "Ekaterinburg", "Tyumen", "Samara", "Volgograd", "Rostov", "Krasnodar",
    ]
    edges = [
        (1200, "SPb", "NNovgorod"), (650, "SPb", "Moscow"),
        (400, "Moscow", "NNovgorod"), (800, "Moscow", "Kazan"),
        (1100, "Moscow", "Rostov"), (400, "NNovgorod", "Kazan"),
        (500, "Kazan", "Ufa"), (450, "Kazan", "Samara"),
        (450, "Ufa", "Samara"), (550, "Ufa", "Ekaterinburg"),
        (350, "Ekaterinburg", "Tyumen"), (850, "Samara", "Volgograd"),
        (900, "Samara", "Rostov"), (400, "Volgograd", "Rostov"),
        (250, "Rostov", "Krasnodar"),
    ]
    mst, total = kruskal(cities, edges)
    print(f"Минимальная суммарная длина сети: {total} км (рёбер: {len(mst)})")
    for u, v, w in mst:
        print(f"  {u} — {v}: {w} км")

    deg = {c: 0 for c in cities}
    for u, v, _ in mst:
        deg[u] += 1
        deg[v] += 1
    max_deg = max(deg.values())
    central = [c for c, d in deg.items() if d == max_deg]
    print(f"Степени городов в MST: {deg}")
    print(f"Центральные города (степень {max_deg}): {central}")

    # Проверка новой дороги Москва — Казань длиной 500 км
    new_edges = [e for e in edges if not ({e[1], e[2]} == {"Moscow", "Kazan"})]
    new_edges.append((500, "Moscow", "Kazan"))
    new_mst, new_total = kruskal(cities, new_edges)
    print(f"После появления дороги Москва—Казань 500 км: общая длина = {new_total} км (MST не изменилось, т.к. путь через Н.Новгород = 400+400, макс. ребро 400 < 500)")


# --- Задание 3: Электрическая сеть (8 подстанций) ---
def task3_power_grid():
    print("=" * 60)
    print("Задание 3. Оптимизация электрической сети (8 подстанций, 15 линий)")
    vertices = ["1", "2", "3", "4", "5", "6", "7", "8"]
    # Примечание: на рисунке подпись линии 2-6 перекрыта подписью 3-5 (2);
    # для определённости принято w(2, 6) = 4.
    edges = [
        (7, "1", "2"), (4, "1", "3"), (6, "1", "4"),
        (6, "2", "3"), (3, "2", "5"), (4, "2", "6"),
        (5, "3", "4"), (2, "3", "5"),
        (7, "4", "6"), (5, "4", "7"),
        (4, "5", "6"), (6, "5", "8"),
        (3, "6", "7"), (5, "6", "8"),
        (2, "7", "8"),
    ]
    k_mst, k_tot = kruskal(vertices, edges)
    p_mst, p_tot = prim(vertices, edges, "1")
    print(f"Краскал (стоимость = {k_tot}): {k_mst}")
    print(f"Прим    (стоимость = {p_tot}): {p_mst}")

    print("Проверка леммы о безопасном ребре для каждого ребра MST:")
    for edge in k_mst:
        s_part, t_part, _, ok = find_cut_for_edge(vertices, k_mst, edges, edge)
        print(f"  Ребро {edge[0]}-{edge[1]} ({edge[2]}): разрез {s_part} | {t_part} -> минимальное? {ok}")

    V, E = len(vertices), len(edges)
    print(f"Оценка операций: Краскал E*log2(E) = {E*math.log2(E):.1f}, Прим E*log2(V) = {E*math.log2(V):.1f}")


if __name__ == "__main__":
    task1_mst_two_ways()
    task2_railways()
    task3_power_grid()
