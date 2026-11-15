import math


# --- Задание 1: Беллман-Форд ---
def task1_bellman_ford():
    print("=" * 60)
    print("Задание 1. Алгоритм Беллмана-Форда (от S до всех вершин)")
    names = ["S", "A", "B", "C", "D", "T"]
    edges = [
        (0, 1, 4),   # S -> A
        (0, 2, 3),   # S -> B
        (1, 2, -2),  # A -> B
        (1, 3, 7),   # A -> C
        (2, 3, 5),   # B -> C
        (2, 4, 8),   # B -> D
        (3, 4, -1),  # C -> D
        (3, 5, 6),   # C -> T
        (4, 5, 3),   # D -> T
    ]
    n = len(names)
    INF = float("inf")
    dist = [INF] * n
    prev = [None] * n
    dist[0] = 0

    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                updated = True
        if not updated:
            break

    # Проверка на отрицательный цикл
    has_neg_cycle = any(dist[u] != INF and dist[u] + w < dist[v] for u, v, w in edges)
    print("Отрицательный цикл:", "Да" if has_neg_cycle else "Нет")
    print("Кратчайшие расстояния от S:")
    for i, name in enumerate(names):
        print(f"  dist[{name}] = {dist[i]}")

    # Восстановление пути до T (индекс 5)
    path = []
    cur = 5
    while cur is not None:
        path.append(names[cur])
        cur = prev[cur]
    path.reverse()
    print(f"Кратчайший путь S -> T: {' -> '.join(path)} (длина = {dist[5]})")


# --- Задание 2: Флойд-Уоршелл ---
def task2_floyd_warshall():
    print("=" * 60)
    print("Задание 2. Алгоритм Флойда-Уоршелла (5 вершин)")
    INF = float("inf")
    # Индексы: 1=0, 2=1, 3=2, 4=3, 5=4
    # Примечание: на рисунке подпись дуги 4->2 перекрывается с 2->4 (-2);
    # т.к. по условию отрицательное ребро одно, принимаем w(2->4)=-2, w(4->2)=4.
    n = 5
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0

    edges = [
        (0, 1, 5),   # 1 -> 2
        (0, 2, 10),  # 1 -> 3
        (1, 2, 3),   # 2 -> 3
        (1, 3, -2),  # 2 -> 4
        (3, 1, 4),   # 4 -> 2
        (2, 3, 2),   # 3 -> 4
        (2, 4, 7),   # 3 -> 5
        (3, 4, 4),   # 4 -> 5
        (4, 0, 12),  # 5 -> 1
    ]
    for u, v, w in edges:
        dist[u][v] = w

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    neg_cycle = any(dist[i][i] < 0 for i in range(n))
    print("Отрицательный цикл:", "Обнаружен" if neg_cycle else "Отсутствует")
    print("Матрица кратчайших расстояний (1..5):")
    print("     " + " ".join(f"{j+1:>4}" for j in range(n)))
    for i in range(n):
        row_str = " ".join(f"{'INF':>4}" if dist[i][j] == INF else f"{dist[i][j]:>4}" for j in range(n))
        print(f"  {i+1}: {row_str}")


# --- Задание 3: Арбитраж валют ---
def task3_arbitrage():
    print("=" * 60)
    print("Задание 3. Финансовый арбитраж валют")
    rates = [
        ("USD", "EUR", 0.85),
        ("EUR", "GBP", 1.15),
        ("GBP", "USD", 1.05),
        ("USD", "JPY", 145.0),
        ("JPY", "GBP", 0.0075),
    ]
    currencies = ["USD", "EUR", "GBP", "JPY"]
    idx = {c: i for i, c in enumerate(currencies)}
    rate_map = {(u, v): r for u, v, r in rates}
    edges = [(idx[u], idx[v], -math.log(r)) for u, v, r in rates]

    n = len(currencies)
    dist = [0.0] * n  # старт со всех вершин одновременно, чтобы найти любой цикл
    prev = [None] * n

    x = -1
    for step in range(n):
        x = -1
        for u, v, w in edges:
            if dist[u] + w < dist[v] - 1e-12:
                dist[v] = dist[u] + w
                prev[v] = u
                x = v

    if x == -1:
        print("Арбитражных возможностей нет.")
        return

    # Входим внутрь отрицательного цикла, сделав n шагов по prev
    for _ in range(n):
        x = prev[x]

    cycle = []
    cur = x
    while True:
        cycle.append(currencies[cur])
        cur = prev[cur]
        if cur == x and len(cycle) > 1:
            break
    cycle.append(currencies[x])
    cycle.reverse()

    product = 1.0
    for i in range(len(cycle) - 1):
        product *= rate_map[(cycle[i], cycle[i + 1])]

    start_capital = 1000.0
    final_capital = start_capital * product
    profit = final_capital - start_capital

    print(f"Найден арбитражный цикл: {' -> '.join(cycle)}")
    print(f"Произведение курсов: {product:.6f}")
    print(f"Итоговая сумма при старте {start_capital:.0f}: {final_capital:.2f} (прибыль = +{profit:.2f})")


if __name__ == "__main__":
    task1_bellman_ford()
    task2_floyd_warshall()
    task3_arbitrage()
