import streamlit as st
from maze_solver import MAZE, START, END, solve_maze_bfs


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
                display_row.append("🔹")  # camino BFS
            elif cell == 1:
                display_row.append("⬛")  # muro
            else:
                display_row.append("⬜")  # libre
        display_maze.append("".join(display_row))

    st.markdown("<br>".join(display_maze), unsafe_allow_html=True)


st.sidebar.header("Opciones")
algorithm = st.sidebar.selectbox(
    "Selecciona el algoritmo",
    ["BFS"]  # Solo tenemos BFS implementado
)
solve_button = st.sidebar.button("Resolver Laberinto")

st.title("Visualizador de Algoritmo de Búsqueda en Laberinto")

# Laberinto inicial
render_maze(MAZE)

if solve_button:
    if algorithm == "BFS":
        path, visited_order, elapsed = solve_maze_bfs(MAZE, START, END)

        if path is not None:
            st.success(
                f"¡Camino encontrado con {algorithm}!  "
                f"Tiempo de ejecución: {elapsed:.5f} segundos  "
                f"(nodos visitados: {len(visited_order)})"
            )

            # Mostrar laberinto con el camino
            st.subheader("Laberinto resuelto")
            render_maze(MAZE, path)

            # Mostrar nodos visitados
            st.subheader("Nodos visitados en orden (fila, columna)")
            for r, c in visited_order:
                st.text(f"visitados {r} {c}")
        else:
            st.error("No se encontró camino usando BFS.")
