import time
import pygame
import numpy as np
from vis_utils import *

# Class to visualize the maze
class VizMap:
    def __init__(self, maze_list):
        self.maze_list = maze_list

        self.width = len(maze_list[0])
        self.height = len(maze_list)

        self.comilones = []

        self.cells = []

        # Goal is denoted by "G" inside of maze_list
        for idx1, inner_list in enumerate(maze_list):
            if "G" in inner_list:
                self.goal = [idx1 + 1, inner_list.index("G") + 1]
            if "S" in inner_list:
                self.start = [idx1 + 1, inner_list.index("S") + 1]

        self.current_cell = None
        self.goal_cell = None

        self.cell_width = (WIDTH - 2 * PADDING) // (self.width + 2)
        self.cell_height = (HEIGHT - 2 * PADDING) // (self.height + 2)

        self.padding_w = (WIDTH - (self.width + 2) * self.cell_width) // 2
        self.padding_h = (HEIGHT - (self.height + 2) * self.cell_height) // 2

        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("DCComilon")

    def time_tick(self):
        done = True
        for idx, comilon in enumerate(self.comilones):
            current_cell = self.maze_list[self.height - comilon.y][comilon.x - 1]

            if current_cell == "G":
                continue

            done = False
            cell_waitime = 1 if current_cell == "A" else 4 if current_cell == "M" else 2
            comilon.wait += 1

            if comilon.wait >= cell_waitime:
                comilon.step += 1
                comilon.wait = 0

        if done:
            time.sleep(2)
            pygame.quit()
            exit()

        time.sleep(SLEEP_TIME)

    def display_maze(self):
        self.display.fill(BLACK)
        for i in range(1, 1 + self.width):
            curr_x = self.padding_w + i * self.cell_width
            for j in range(1, 1 + self.height):
                curr_y = self.padding_h + j * self.cell_height
                cell = self.maze_list[j - 1][i - 1]

                if cell == "S":
                    pygame.draw.rect(self.display, CHARACTER_COLOR, (curr_x + self.cell_width // 12, curr_y + self.cell_height // 12, 5 * self.cell_width // 6, 5 * self.cell_height // 6))
                elif cell == "G":
                    # pygame.draw.rect(self.display, WHITE, (curr_x, curr_y, self.cell_width, self.cell_height))
                    draw_burger(curr_x, curr_y, self.cell_width, self.display, outline = False)

                elif cell == "A":
                    # pygame.draw.circle(self.display, RED, (curr_x + self.cell_width // 2, curr_y + self.cell_height // 2), self.cell_width // 4)
                    draw_chili(curr_x + self.cell_width // 6, curr_y + self.cell_height // 6, 2 * self.cell_width // 3, self.display)
                elif cell == "M":
                    pygame.draw.circle(self.display, YELLOW, (curr_x + self.cell_width // 2, curr_y + self.cell_height // 2), self.cell_width // 4)

        draw_walls(self.cell_width, self.cell_height, self.padding_w, self.padding_h, self.maze_list, self.display)

        for idx, comilon in enumerate(self.comilones):
            self.draw_comilon_trail(comilon, idx)
            comilon.draw(self.cell_width, self.cell_height, self.display, self.height, self.padding_w, self.padding_h)

        pygame.display.update()

    def add_comilon(self, size, comilon_path, color = CHARACTER_COLOR):
        if len(comilon_path) == 0:
            return
        
        self.comilones.append(Comilon(size, comilon_path, color))

    def draw_comilon_trail(self, comilon, idx):
        curr_x = self.padding_w + self.start[1] * self.cell_width
        curr_y = self.padding_h + self.start[0] * self.cell_height

        total_comilones = len(self.comilones)
        fillable_area = self.cell_width // 3
        offset = (self.cell_width - fillable_area) // 2 + idx * fillable_area // total_comilones
        width = max(1, (2 * self.cell_width // 3) // total_comilones // 4)

        for i in range(min(comilon.step + 1, len(comilon.path))):
            new_x = self.padding_w + comilon.path[i][0] * self.cell_width
            new_y = self.padding_h + (self.height - comilon.path[i][1] + 1) * self.cell_height

            pygame.draw.line(self.display, comilon.color, (curr_x + offset, curr_y + offset), (new_x + offset, new_y + offset), width)
            curr_x, curr_y = new_x, new_y

if __name__ == "__main__":
    path_map = "DCComilon/tests/test_4.txt"

    with open(path_map, "r") as file:
        maze_list_raw = file.readlines()
    maze_list = []
    for line in maze_list_raw:
        maze_list.append(line.strip("\n").split(" "))

    astar_path = list(reversed([[25, 8], [25, 7], [25, 6], [25, 5], [26, 5], [27, 5], [27, 6], [27, 7], [27, 8], [27, 9], [27, 10], [26, 10], [25, 10], [25, 11], [25, 12], [25, 13], [25, 14], [25, 15], [25, 16], [24, 16], [23, 16], [23, 15], [23, 14], [23, 13], [23, 12], [22, 12], [21, 12], [21, 11], [21, 10], [21, 9], [21, 8], [21, 7], [21, 6], [20, 6], [19, 6], [19, 5], [19, 4], [19, 3], [18, 3], [17, 3], [17, 2], [17, 1], [16, 1], [15, 1], [14, 1], [13, 1], [12, 1], [11, 1], [11, 2], [11, 3], [10, 3], [9, 3], [9, 4], [8, 4], [7, 4], [7, 3], [7, 2], [7, 1], [6, 1], [5, 1], [4, 1], [3, 1], [2, 1], [1, 1], [1, 2], [1, 3], [1, 4], [2, 4], [3, 4], [3, 3], [4, 3], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [5, 12], [5, 13], [5, 14], [4, 14], [3, 14], [3, 15], [3, 16], [3, 17], [3, 18], [3, 19], [3, 20], [3, 21], [3, 22], [2, 22], [1, 22], [1, 23], [1, 24], [1, 25], [1, 26], [2, 26], [3, 26], [4, 26], [5, 26], [5, 25], [5, 24], [4, 24], [3, 24]]))
    dfs_path = list(reversed([[25, 8], [25, 7], [25, 6], [25, 5], [26, 5], [27, 5], [27, 6], [27, 7], [27, 8], [27, 9], [27, 10], [26, 10], [25, 10], [25, 11], [25, 12], [25, 13], [25, 14], [25, 15], [25, 16], [24, 16], [23, 16], [23, 15], [23, 14], [23, 13], [23, 12], [22, 12], [21, 12], [21, 13], [21, 14], [21, 15], [21, 16], [21, 17], [21, 18], [22, 18], [23, 18], [24, 18], [25, 18], [25, 19], [25, 20], [25, 21], [24, 21], [23, 21], [23, 22], [22, 22], [21, 22], [20, 22], [19, 22], [18, 22], [17, 22], [17, 23], [17, 24], [16, 24], [15, 24], [14, 24], [13, 24], [13, 25], [13, 26], [12, 26], [11, 26], [10, 26], [9, 26], [9, 25], [9, 24], [9, 23], [9, 22], [8, 22], [7, 22], [7, 21], [7, 20], [7, 19], [7, 18], [7, 17], [7, 16], [7, 15], [7, 14], [7, 13], [7, 12], [7, 11], [7, 10], [6, 10], [5, 10], [5, 11], [5, 12], [5, 13], [5, 14], [4, 14], [3, 14], [3, 15], [3, 16], [3, 17], [3, 18], [3, 19], [3, 20], [3, 21], [3, 22], [2, 22], [1, 22], [1, 23], [1, 24], [1, 25], [1, 26], [2, 26], [3, 26], [4, 26], [5, 26], [5, 25], [5, 24], [4, 24], [3, 24]]))

    viz = VizMap(maze_list)
    viz.add_comilon(3 * viz.cell_width // 4, astar_path)
    viz.add_comilon(3 * viz.cell_width // 4, dfs_path, color = BLUE)
    
    while True:
        viz.time_tick()
        viz.display_maze()