import streamlit as st
from maze_solver import MAZE, START, END, solve_maze_bfs, solve_maze_dfs, solve_maze_astar


def render_maze(maze, path=None):
    """Dibuja el laberinto con emojis."""
    if path is None:
        path = []

    display_maze = []
    for r_idx, row in enumerate(maze):
        display_row = []
        for c_idx, cell in enumerate(row):
            pos = (r_idx, c_idx)

            if pos == START:
                display_row.append("🚀")  # inicio
            elif pos == END:
                display_row.append("🏁")  # meta
            elif pos in path:
                display_row.append("🔹")  # camino
            elif cell == 1:
                display_row.append("⬛")  # muro
            else:
                display_row.append("⬜")  # libre

        display_maze.append("".join(display_row))

    st.markdown("<br>".join(display_maze), unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
st.sidebar.header("Opciones")

algorithm = st.sidebar.selectbox(
    "Selecciona el algoritmo",
    ["BFS", "DFS", "A*"]
)

solve_button = st.sidebar.button("Resolver Laberinto")


# ---------------- INTERFAZ PRINCIPAL ----------------
st.title("Visualizador de Algoritmos de Búsqueda en Laberinto")

# Mostrar laberinto inicial
st.subheader("Laberinto")
render_maze(MAZE)


# ---------------- RESOLUCIÓN ----------------
if solve_button:

    if algorithm == "BFS":
        path, visited_order, elapsed = solve_maze_bfs(MAZE, START, END)

    elif algorithm == "DFS":
        path, visited_order, elapsed = solve_maze_dfs(MAZE, START, END)

    else:   # A*
        path, visited_order, elapsed = solve_maze_astar(MAZE, START, END)

    # Mostrar resultados
    if path is not None:
        st.success(
            f"Camino encontrado con {algorithm} | "
            f"Tiempo de ejecución: {elapsed:.5f} segundos | "
            f"Nodos visitados: {len(visited_order)}"
        )

        # Mostrar laberinto con solución
        st.subheader("Laberinto resuelto")
        render_maze(MAZE, path)

        # Mostrar nodos visitados
        st.subheader("Nodos visitados en orden (fila, columna)")
        for r, c in visited_order:
            st.text(f"visitados {r} {c}")

    else:
        st.error(f"No se encontró camino usando {algorithm}.")
