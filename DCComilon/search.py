# CONTIENE LOS ALGORITMOS DE BUSQUEDA
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
    t_start = time.perf_counter()
    
    open = [s_init]
    expansions = 1
    closed = []

    while len(open) != 0:
        u = open.pop(0)
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

def inverted_dfs(s_init, s_goal):
    """
    s_init y s_goal son objetos de clase cell. Retorna el nodo objetivo
    de clase cell en caso de encontrarlo.
    """

    # COMPLETAR
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
        succ = list(reversed([move[1] for move in moves]))

        # Para cada sucesor:
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


# ----------------------- Actividad 2.2 -----------------------------
def a_star(s_init, s_goal,h):
    """
    s_init y s_goal son objetos de clase cell. Retorna el nodo objetivo
    de clase cell en caso de encontrarlo.
    Open ordenado segun el valor de f

    h es la funcion heuristica que quieres usar ie 'manhattan' o 'euclidian'
    """
    t_start = time.perf_counter()
    heur=heuristic(h)
    open = [s_init]
    s_init.g = 0
    s_init.h=heur(s_init,s_goal)
    
    s_init.f=s_init.h
    expansions = 1
    open = [s_init]
    

    while len(open) != 0:
        u = open.pop()
        
        if u.cell_type == "G":
            t_end = time.perf_counter()
            t_total = (t_end - t_start ) * 1000
            print(f"heuristic used: {h}")
            print(f"Tiempo de ejecución: {t_total:.10f} ms")
            print("Número de expansiones: {}".format(expansions))
            print("Largo del camino encontrado: {}".format(len(get_parents(s_goal))))
            print("Costo total del camino: {}".format(get_cost(s_goal)))
            return (u, get_parents(s_goal))
        
        expansions += 1

        # Obtenemos las posibles acciones:
        moves = u.get_moves()
        succ = [move[1] for move in moves]
        
        # Para cada sucesor...
        for v in succ:
            is_new=False
            c_v=u.g+v.cost
            
            if v.g==1000000000: #is_new if the cost of v is the default cost for a cell
                is_new=True
            if is_new or c_v<v.g:
                v.parent=u
                v.g=c_v
                v.h=heur(v,s_goal)
                v.f=v.g+v.h
                if is_new:
                    open=insertar(open,v)
                    
                else:
                    open=reordenar(open)
    
    return [], []

def reordenar(op):
    sorted_op = sorted(op, key=lambda cell: cell.f, reverse=True)
    return sorted_op
    
def ordenar(succ):
    sorted_succ = sorted(succ, key=lambda cell: cell.F, reverse=True)
    return sorted_succ


def insertar(op,new):
    if len(op)==0:
        op.append(new)
        
    else:
        index = 0
        while index < len(op) and op[index].f >= new.f:
            index += 1
        op.insert(index, new)
    return op

def heuristic_manhattan(cell, goal):
        return (abs(cell.pos_x-goal.pos_x)+abs(cell.pos_y-goal.pos_y))//2
def heuristic_euclidian(cell, goal):
        return (((cell.pos_x-goal.pos_x)**2 + (cell.pos_y-goal.pos_y)**2)**0.5)//2


def heuristic(re):
    def h_manhattan(cell, goal):
        return (abs(cell.pos_x-goal.pos_x)+abs(cell.pos_y-goal.pos_y))//2
    
    def h_euclidian(cell, goal):
        return (((cell.pos_x-goal.pos_x)**2 + (cell.pos_y-goal.pos_y)**2)**0.5)//2

    if re=='manhattan':
        return h_manhattan
    elif re=='euclidian':
        return h_euclidian


# ----------------------- Actividad 2.3 -----------------------------

# ----- RBFS
def recursive_best_first_search(s_init,s_goal,h,expan):
    heur=heuristic(h)
    t_start = time.perf_counter()
    closed=[]
    S=s_init
    B=float('inf')
    s_init.g=0
    
    s_init.h=heur(s_init,s_goal)
    s_init.f=s_init.g+s_init.h
    closed.append(s_init)
    sol,b=RBFS(s_init,s_goal,B,heur,expan,S)
    t_end = time.perf_counter()
    t_total = (t_end - t_start ) * 1000
    
    print(f"Tiempo de ejecución: {t_total:.10f} ms")
    print("Número de expansiones: {}".format(expan))
    print("Largo del camino encontrado: {}".format(len(get_parents(s_goal))))
    print("Costo total del camino: {}".format(get_cost_rbgs(S,s_goal)))
    return (sol, get_parents(s_goal))

        
def RBFS(node,s_goal,f_limit,he,exp,S) : 
    print("\nIn RBFS Function with node ", node.cell_type, " with node's f value = ", node.f , " and f-limit = ", f_limit)
    
    if node.cell_type=='G':
        return node,None 
    
    moves = node.get_moves()
    succ = [move[1] for move in moves]
    successors=[]
    exp+=1
    print(succ)
    
    for i in range(len(succ)):
        child=succ[i]
        
        if node.parent!=None and child.pos_x!=node.parent.pos_x and child.pos_y!=node.parent.pos_y:

            child.parent=node
            
            child.g=get_cost_rbgs(S,node)+child.cost
            
            child.h = he(child,s_goal)
            child.f = max(child.g+child.h , node.f)
            successors.append(child)
        elif node.parent==None and child.pos_x!=S.pos_x or child.pos_y!=S.pos_y:
            
            child.parent=node
            
            child.g=get_cost_rbgs(S,node)+child.cost
            
            child.h = he(child,s_goal)
            child.f = max(child.g+child.h , node.f)
            successors.append(child)
        
    if len(successors) == 0 :
        
        return [None, float('inf')]
    while True:  
        
        successors=reordenar(successors)    
        best  = successors[-1]
        
        if best.f > f_limit :
            return [None, best.f]
        alter = successors[-2].f if len(successors)>1 else float('inf')
     
        x = RBFS(best,s_goal, min(f_limit, alter),he,exp,S)
        result = x[0]        
        best.f = x[1]                    
        if result != None :
            return [result, None]
 

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

#Fue agregado para el recursive best first search
def get_cost_rbgs(S,cell):
    nodo_actual = cell
    total_cost = nodo_actual.cost
    while nodo_actual.pos_x!=S.pos_x or nodo_actual.pos_y!=S.pos_y :
        nodo_actual = nodo_actual.parent
        total_cost += nodo_actual.cost
    return total_cost
