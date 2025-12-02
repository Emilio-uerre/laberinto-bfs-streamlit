import streamlit as st
from maze_solver import MAZE, START, END, solve_maze_bfs, solve_maze_dfs


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
                display_row.append("🔹")  # camino encontrado
            elif cell == 1:
                display_row.append("⬛")  # muro
            else:
                display_row.append("⬜")  # libre
        display_maze.append("".join(display_row))

    st.markdown("<br>".join(display_maze), unsafe_allow_html=True)


# ----------- UI LATERAL -----------
st.sidebar.header("Opciones")
algorithm = st.sidebar.selectbox(
    "Selecciona el algoritmo",
    ["BFS", "DFS"]
)
solve_button = st.sidebar.button("Resolver Laberinto")

# ----------- TÍTULO Y LABERINTO INICIAL -----------
st.title("Visualizador de Algoritmo de Búsqueda en Laberinto")
render_maze(MAZE)

# ----------- RESOLVER SEGÚN ALGORITMO -----------
if solve_button:
    # Elegir algoritmo
    if algorithm == "BFS":
        path, visited_order, elapsed = solve_maze_bfs(MAZE, START, END)
    else:  # DFS
        path, visited_order, elapsed = solve_maze_dfs(MAZE, START, END)

    # Mostrar resultados
    if path is not None:
        st.success(
            f"¡Camino encontrado con {algorithm}!  "
            f"Tiempo de ejecución: {elapsed:.5f} segundos  "
            f"(nodos visitados: {len(visited_order)})"
        )

        # Laberinto con el camino marcado
        st.subheader("Laberinto resuelto")
        render_maze(MAZE, path)

        # Nodos visitados
        st.subheader("Nodos visitados en orden (fila, columna)")
        for r, c in visited_order:
            st.text(f"visitados {r} {c}")
    else:
        st.error(f"No se encontró camino usando {algorithm}.")
