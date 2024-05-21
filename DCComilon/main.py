import os
from visualization import VizMap
from search import bfs, dfs, recursive_best_first_search, a_star, inverted_dfs

CWD = os.path.dirname(__file__)

viz = True
MAP_PATH = f"{CWD}/tests/test_4.txt"

ASTAR_COLOR = (255, 200, 64)
DFS_COLOR = (234, 130, 229)
BFS_COLOR = (70, 191, 238)
RBFS_COLOR = (208, 62, 25)
IDFS_COLOR = (219, 133, 28)

class Cell:
    def __init__(self, pos_x, pos_y, cell_type):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cell_type = cell_type
        self.cost = 1
        self.parent = None

        self.right_neigh = None
        self.left_neigh = None
        self.top_neigh = None
        self.down_neigh = None

    def __str__(self):
        if (self.cell_type == "P"):
            return " "
        else:
            return self.cell_type

    def __repr__(self):
        return f"{self.cell_type}"
    
    def get_moves(self):
        moves = []
        if self.top_neigh is not None:
            if self.top_neigh.cell_type != "B":
                moves.append(["u", self.top_neigh])
        if self.down_neigh is not None:
            if self.down_neigh.cell_type != "B":
                moves.append(["d", self.down_neigh])
        if self.right_neigh is not None:
            if self.right_neigh.cell_type != "B":
                moves.append(["r", self.right_neigh])
        if self.left_neigh is not None:
            if self.left_neigh.cell_type != "B":
                moves.append(["l", self.left_neigh])
    
        return moves

class Maze:
    def __init__(self):
        self.cells = []
        self.goal = None
        self.start = None
        self.current_cell = None
        self.goal_cell = None
        pass

    def create_maze(self, maze_list):
        maze_list = maze_list[::-1] # invertimos la lista para comenzar x=0 e y=0 en la esq inferior izq como plano cartesiano 
        
        self.cells.append([Cell(pos_x=e, pos_y=0, cell_type="B") for e in range(len(maze_list[0]) + 2)])
        
        for i in range(len(maze_list)):
            self.cells.append([])
            self.cells[i+1].append(Cell(pos_x=0, pos_y=i+1, cell_type="B"))

            for a in range(len(maze_list[0])):
                self.cells[i+1].append(Cell(pos_x=a+1, pos_y=i+1, cell_type=maze_list[i][a]))
                if maze_list[i][a] == "G":
                    self.goal = (a+1, i+1)
                    self.goal_cell = self.cells[i+1][a+1]
                if maze_list[i][a] == "S":
                    self.start = (a+1, i+1)
                    self.current_cell = self.cells[i+1][a+1]
                if maze_list[i][a] == "A":
                    self.cells[i+1][a+1].cost = 0.5
                if maze_list[i][a] == "M":
                    self.cells[i+1][a+1].cost = 2
                
                    
            self.cells[i+1].append(Cell(pos_x=len(maze_list[0])+1, pos_y=i+1, cell_type="B"))
        
        self.cells.append([Cell(pos_x=i, pos_y=len(maze_list)+1, cell_type="B") for i in range(len(maze_list[0]) + 2)])
        self.cells = self.cells[::-1]
        self.set_neighbours()
    
    def set_neighbours(self):
        self.cells = self.cells[::-1]
        for i in range(1, len(self.cells)-1):
            for a in range(1, len(self.cells[0])-1):
                self.cells[i][a].right_neigh = self.cells[i][a+1] if a+1 < len(self.cells[0]) else None
                self.cells[i][a].left_neigh = self.cells[i][a-1] if a-1 > 0 else None
                self.cells[i][a].top_neigh = self.cells[i+1][a] if i+1 < len(self.cells) else None
                self.cells[i][a].down_neigh = self.cells[i-1][a] if i-1 > 0 else None
        self.cells = self.cells[::-1]

    def print_maze(self, parents_list):
        print("-"*4*len(self.cells[0]))
        for i in range(len(self.cells)):
            row = "|"
            for a in range(len(self.cells[0])):
                if [self.cells[i][a].pos_x, self.cells[i][a].pos_y] in parents_list:
                    if str(self.cells[i][a]) == " ":
                        row += colortext("*").green()
                    else:
                        row += colortext(str(self.cells[i][a])).green()
                else:
                    row += str(self.cells[i][a])
                row += " | "
            print(row)
            print("-"*4*len(self.cells[0]))
        print(f"El comienzo es: {self.start}")
        print(f"La meta es: {self.goal}")

    def __getitem__(self, indieces):
        x = indieces[0]
        y = indieces[1]
        return self.cells[len(self.cells)-y-1][x]

if __name__ == "__main__":
    
    class colortext():
        def __init__(self, text:str):
            self.text = text
            self.ending = '\033[0m'

        def green(self):
            return '\033[91m' + self.text + self.ending

    with open(MAP_PATH, "r") as file:
        maze_list_raw = file.readlines()
    maze_list = []
    for line in maze_list_raw:
        maze_list.append(line.strip("\n").split(" "))

    maze = Maze()
    maze.create_maze(maze_list)

    print(f"\nDFS\n{10 * '-'}")
    objetivo_dfs, parents_list_dfs = dfs(maze.current_cell, maze.goal_cell)
    
    print(f"\nInverted DFS\n{10 * '-'}")
    objetivo_idfs, parents_list_idfs = inverted_dfs(maze.current_cell, maze.goal_cell)

    print(f"\nBFS\n{10 * '-'}")
    objetivo_bfs, parents_list_bfs = bfs(maze.current_cell, maze.goal_cell)

    print(f"\nRBFS\n{10 * '-'}")
    objetivo_rbfs, parents_list_rbfs = recursive_best_first_search(maze.current_cell, maze.goal_cell)

    print(f"\nA*\n{10 * '-'}")
    objetivo_a_star, parents_list_a_star = a_star(maze.current_cell, maze.goal_cell)

    if viz:
        viz = VizMap(maze_list)

        # Add the DFS comilon
        viz.add_comilon(3 * viz.cell_width // 4, list(reversed(parents_list_dfs)), color = DFS_COLOR)

        # Add the IDFS comilon
        viz.add_comilon(3 * viz.cell_width // 4, list(reversed(parents_list_idfs)), color = IDFS_COLOR)
        
        # Add the BFS comilon
        viz.add_comilon(3 * viz.cell_width // 4, list(reversed(parents_list_bfs)), color = BFS_COLOR)

        # Add the RBFS comilon
        viz.add_comilon(3 * viz.cell_width // 4, list(reversed(parents_list_rbfs)), color = RBFS_COLOR)

        # Add the A* comilon
        viz.add_comilon(3 * viz.cell_width // 4, list(reversed(parents_list_a_star)), color = ASTAR_COLOR)


        while True:
            viz.display_maze()
            viz.time_tick()