from collections import deque
import time
import heapq

# Laberinto del ejercicio
# 0 = libre, 1 = muro
MAZE = [
[1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1],
[1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1],
[1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1],
[1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1],
[1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1],
[1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1],
[1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,1],
[1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1],
[1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,1],
[1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1],
[1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,1],
[1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1],
[1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1],
[1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
[1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,1],
[1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1],
[1,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,1],
[1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1],
[1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,1],
[1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1],
[1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1,1],
[1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,1],
[1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1],
[1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1],
[1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,1],
[1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1],
[1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1],
[1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1],
[1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1],
[1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1],
[1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,1],
[1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1],
[1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,0,1],
[1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1],
[1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1]
]

# Coordenadas inicio y meta (fila, columna)
START = (0, 1)
END   = (36, 30)


def solve_maze_bfs(maze, start, end):
    """
    Resuelve el laberinto usando BFS.

    Regresa:
        path: lista con el camino desde start hasta end
        visited_order: lista con los nodos visitados en orden
        elapsed: tiempo de ejecución en segundos
    """
    rows, cols = len(maze), len(maze[0])

    start_time = time.time()

    queue = deque([(start, [start])])
    visited = set([start])
    visited_order = []

    while queue:
        (r, c), path = queue.popleft()

        # Registrar nodo visitado
        visited_order.append((r, c))

        # ¿Llegamos a la meta?
        if (r, c) == end:
            elapsed = time.time() - start_time
            return path, visited_order, elapsed

        # Movimientos: arriba, abajo, izquierda, derecha
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc

            if (
                0 <= nr < rows and
                0 <= nc < cols and
                maze[nr][nc] == 0 and
                (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                new_path = list(path)
                new_path.append((nr, nc))
                queue.append(((nr, nc), new_path))

    # No se encontró camino
    elapsed = time.time() - start_time
    return None, visited_order, elapsed

def solve_maze_dfs(maze, start, end):
    import time
    rows, cols = len(maze), len(maze[0])
    start_time = time.perf_counter()

    stack = [(start, [start])]
    visited = set([start])
    visited_order = []

    while stack:
        (r, c), path = stack.pop()
        visited_order.append((r, c))

        if (r, c) == end:
            elapsed = time.perf_counter() - start_time
            return path, visited_order, elapsed

        # Orden de exploración DFS
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc

            if (
                0 <= nr < rows and
                0 <= nc < cols and
                maze[nr][nc] == 0 and
                (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                stack.append(((nr, nc), path + [(nr, nc)]))

    elapsed = time.perf_counter() - start_time
    return None, visited_order, elapsed

def _manhattan(a, b):
    """Heurística de distancia Manhattan para A*."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve_maze_astar(maze, start, end):
    """
    Resuelve el laberinto usando el algoritmo A*.

    Regresa:
        path: lista con el camino desde start hasta end
        visited_order: nodos visitados en el orden en que se extraen de la cola
        elapsed: tiempo de ejecución en segundos
    """
    rows, cols = len(maze), len(maze[0])
    start_time = time.perf_counter()

    # open_set: (f, g, (r, c), path)
    open_set = []
    start_h = _manhattan(start, end)
    heapq.heappush(open_set, (start_h, 0, start, [start]))

    visited = set()
    visited_order = []

    while open_set:
        f, g, (r, c), path = heapq.heappop(open_set)

        if (r, c) in visited:
            continue

        visited.add((r, c))
        visited_order.append((r, c))

        # ¿Llegamos a la meta?
        if (r, c) == end:
            elapsed = time.perf_counter() - start_time
            return path, visited_order, elapsed

        # Movimientos válidos (4 direcciones)
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc

            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and maze[nr][nc] == 0
                and (nr, nc) not in visited
            ):
                g2 = g + 1  # costo acumulado
                h2 = _manhattan((nr, nc), end)
                f2 = g2 + h2
                heapq.heappush(open_set, (f2, g2, (nr, nc), path + [(nr, nc)]))

    # No se encontró camino
    elapsed = time.perf_counter() - start_time
    return None, visited_order, elapsed
