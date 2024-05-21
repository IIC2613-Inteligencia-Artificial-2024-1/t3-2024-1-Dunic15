# CONTIENE LOS ALGORITMOS DE BÚSQUEDA
import time

# ----- DFS
def dfs(s_init, s_goal):
    """
    s_init y s_goal son objetos de clase cell. Retorna el nodo objetivo
    de clase cell en caso de encontrarlo.
    """
    t_start = time.perf_counter()

    open = [s_init]
    expansions = 1
    closed = []

    while len(open) != 0:
        u = open.pop()
        expansions += 1
        closed.append(u)

        # Obtenemos las posibles acciones:
        moves = u.get_moves()
        succ = [move[1] for move in moves]

        # Para cada sucesor...
        for v in succ:
            if v not in open and v not in closed:
                v.parent = u
                if v.cell_type == "G":
                    t_end = time.perf_counter()
                    t_total = (t_end - t_start ) * 1000
                    print(f"Tiempo de ejecución: {t_total:.10f} ms")
                    print("Número de expansiones: {}".format(expansions))
                    print("Largo del camino encontrado: {}".format(len(get_parents(s_goal))))
                    print("Costo total del camino: {}".format(get_cost(s_goal)))
                    return (v, get_parents(s_goal))
                open.append(v)
    return [], []


# ----------------------- Actividad 2.1 -----------------------------
def bfs(s_init, s_goal):
    # COMPLETAR
    return [], []

def inverted_dfs(s_init, s_goal):
    # COMPLETAR
    return [], []


# ----------------------- Actividad 2.2 -----------------------------
def a_star(s_init, s_goal):
    # COMPLETAR
    return [], []

def heuristic_manhattan(cell, goal):
    # COMPLETAR
    pass

def heuristic_euclidian(cell, goal):
    # COMPLETAR
    pass


# ----------------------- Actividad 2.3 -----------------------------
def recursive_best_first_search(s_init, s_goal):
    # COMPLETAR
    return [], []

        

# Funciones útiles para usar en algoritmos de búsqueda (ver implementación de dfs)
def get_parents(cell):
    """
    Recibe una celda y retorna la cadena de parents hasta la celda de inicio.
    """
    nodo_actual = cell
    parents = [[nodo_actual.pos_x, nodo_actual.pos_y]]
    while nodo_actual.parent is not None:
        parents.append([nodo_actual.parent.pos_x, nodo_actual.parent.pos_y])
        nodo_actual = nodo_actual.parent

    return parents

def get_cost(cell):
    nodo_actual = cell
    total_cost = nodo_actual.cost
    while nodo_actual.parent is not None:
        nodo_actual = nodo_actual.parent
        total_cost += nodo_actual.cost
    return total_cost