import pygame
import numpy as np

WIDTH = 800
HEIGHT = 800
PADDING = 20
FPS = 15
SLEEP_TIME = 1/FPS

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
BUN_COLOR_LIGHT = (234, 214, 173)
BUN_COLOR = (228, 167, 115)
BURGER_COLOR = (113, 64, 56)

WALL_COLOR = (13, 78, 238)

WHITE = (255, 255, 255)
ICE_COLOR = (154, 214, 232)
BLUE = (74, 93, 171)

CHARACTER_COLOR = (255, 200, 64)
INSIDE_FILL = 6

class Comilon:
    def __init__(self, size, path, color = CHARACTER_COLOR):
        self.size = size
        self.x = path[0][0]
        self.y = path[0][1]
        self.color = color

        self.path = path
        self._wait = 0
        self._step = 0
        self.current_cost = 2

        self.facing = "right"
        self.mouth_open = False

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        if value >= len(self.path):
            return
        
        self._step = value
        new_x, new_y = self.path[value]

        if new_x > self.x:
            self.facing = "right"
        elif new_x < self.x:
            self.facing = "left"
        elif new_y > self.y:
            self.facing = "up"
        elif new_y < self.y:
            self.facing = "down"
        self.x, self.y = new_x, new_y

    @property
    def wait(self):
        return self._wait

    @wait.setter
    def wait(self, value):
        self._wait = value
        self.mouth_open = not self.mouth_open

    def draw(self, cell_width, cell_height, display, map_height, pad_w = PADDING, pad_h = PADDING):
        curr_x = pad_w + self.x * cell_width
        curr_y = pad_h + (map_height - self.y + 1) * cell_height

        pygame.draw.circle(display, self.color, (curr_x + cell_width // 2, curr_y + cell_height // 2), self.size // 2)

        if self.mouth_open:
            if self.facing == "right":
                pygame.draw.polygon(display, BLACK, [(curr_x + cell_width // 2, curr_y + cell_height // 2), (curr_x + cell_width, curr_y + 2 * cell_height // 3), (curr_x + cell_width, curr_y + cell_height // 3)])
            elif self.facing == "left":
                pygame.draw.polygon(display, BLACK, [(curr_x + cell_width // 2, curr_y + cell_height // 2), (curr_x, curr_y + 2 * cell_height // 3), (curr_x, curr_y + cell_height // 3)])
            elif self.facing == "up":
                pygame.draw.polygon(display, BLACK, [(curr_x + cell_width // 2, curr_y + cell_height // 2), (curr_x + 2 * cell_width // 3, curr_y), (curr_x + cell_width // 3, curr_y)])
            elif self.facing == "down":
                pygame.draw.polygon(display, BLACK, [(curr_x + cell_width // 2, curr_y + cell_height // 2), (curr_x + 2 * cell_width // 3, curr_y + cell_height), (curr_x + cell_width // 3, curr_y + cell_height)])

        else:
            if self.facing == "right":
                pygame.draw.polygon(display, BLACK, [(curr_x + cell_width // 2, curr_y + cell_height // 2), (curr_x + cell_width, curr_y + cell_height), (curr_x + cell_width, curr_y)])
            elif self.facing == "left":
                pygame.draw.polygon(display, BLACK, [(curr_x + cell_width // 2, curr_y + cell_height // 2), (curr_x, curr_y + cell_height), (curr_x, curr_y)])
            elif self.facing == "up":
                pygame.draw.polygon(display, BLACK, [(curr_x + cell_width // 2, curr_y + cell_height // 2), (curr_x + cell_width, curr_y), (curr_x, curr_y)])
            elif self.facing == "down":
                pygame.draw.polygon(display, BLACK, [(curr_x + cell_width // 2, curr_y + cell_height // 2), (curr_x + cell_width, curr_y + cell_height), (curr_x, curr_y + cell_height)])

def draw_chili(x, y, size, display):

    total_cells = 8
    cell_size = size // total_cells

    padding_width = (size - 7 * cell_size) // 2
    padding_height = (size - 8 * cell_size) // 2

    # Draw the chili's hat
    pygame.draw.rect(display, GREEN, (padding_width + x + 2 * cell_size, padding_height + y + 0 * cell_size, 1 * cell_size, 1 * cell_size))
    pygame.draw.rect(display, GREEN, (padding_width + x + 1 * cell_size, padding_height + y + 1 * cell_size, 1 * cell_size, 2 * cell_size))
    pygame.draw.rect(display, GREEN, (padding_width + x + 0 * cell_size, padding_height + y + 2 * cell_size, 2 * cell_size, 1 * cell_size))

    # Draw the chili's body
    pygame.draw.rect(display, RED, (padding_width + x + 0 * cell_size, padding_height + y + 3 * cell_size, 3 * cell_size, 3 * cell_size))
    pygame.draw.rect(display, RED, (padding_width + x + 0 * cell_size, padding_height + y + 4 * cell_size, 4 * cell_size, 2 * cell_size))
    pygame.draw.rect(display, RED, (padding_width + x + 1 * cell_size, padding_height + y + 5 * cell_size, 4 * cell_size, 2 * cell_size))
    pygame.draw.rect(display, RED, (padding_width + x + 1 * cell_size, padding_height + y + 6 * cell_size, 6 * cell_size, 1 * cell_size))
    pygame.draw.rect(display, RED, (padding_width + x + 2 * cell_size, padding_height + y + 6 * cell_size, 4 * cell_size, 2 * cell_size))
    pygame.draw.rect(display, WHITE, (padding_width + x + 2 * cell_size, padding_height + y + 4 * cell_size, 1 * cell_size, 1 * cell_size))
    pygame.draw.rect(display, WHITE, (padding_width + x + 3 * cell_size, padding_height + y + 5 * cell_size, 1 * cell_size, 1 * cell_size))

def draw_burger(x, y, size, display, outline = False):

    total_cells = 8
    cell_size = size // total_cells

    padding_width = (size - 8 * cell_size) // 2
    padding_height = (size - 8 * cell_size) // 2

    if outline:
        pygame.draw.rect(display, WHITE, (padding_width + x + -1 * cell_size, padding_height + y + 0 * cell_size, 10 * cell_size, 9 * cell_size))
        pygame.draw.rect(display, WHITE, (padding_width + x + 0 * cell_size, padding_height + y + -1 * cell_size, 8 * cell_size, 10 * cell_size))

    # Draw the burger's bun
    pygame.draw.rect(display, BUN_COLOR, (padding_width + x + 0 * cell_size, padding_height + y + 1 * cell_size, 8 * cell_size, 7 * cell_size))
    pygame.draw.rect(display, BUN_COLOR, (padding_width + x + 1 * cell_size, padding_height + y + 0 * cell_size, 6 * cell_size, 8 * cell_size))
    pygame.draw.rect(display, BUN_COLOR_LIGHT, (padding_width + x + 0 * cell_size, padding_height + y + 4 * cell_size, 8 * cell_size, 2 * cell_size))
    pygame.draw.rect(display, BUN_COLOR_LIGHT, (padding_width + x + 7 * cell_size, padding_height + y + 3 * cell_size, 1 * cell_size, 1 * cell_size))
    pygame.draw.rect(display, BUN_COLOR_LIGHT, (padding_width + x + 2 * cell_size, padding_height + y + 1 * cell_size, 1 * cell_size, 1 * cell_size))
    pygame.draw.rect(display, BUN_COLOR_LIGHT, (padding_width + x + 4 * cell_size, padding_height + y + 2 * cell_size, 1 * cell_size, 1 * cell_size))
    pygame.draw.rect(display, BUN_COLOR_LIGHT, (padding_width + x + 5 * cell_size, padding_height + y + 0 * cell_size, 1 * cell_size, 1 * cell_size))

    # Draw the burger's fillings
    pygame.draw.rect(display, BURGER_COLOR, (padding_width + x + 1 * cell_size, padding_height + y + 5 * cell_size, 6 * cell_size, 2 * cell_size))
    pygame.draw.rect(display, GREEN, (padding_width + x + 0 * cell_size, padding_height + y + 5 * cell_size, 8 * cell_size, 1 * cell_size))
    pygame.draw.rect(display, YELLOW, (padding_width + x + 4 * cell_size, padding_height + y + 5 * cell_size, 3 * cell_size, 1 * cell_size))
    pygame.draw.rect(display, RED, (padding_width + x + 0 * cell_size, padding_height + y + 5 * cell_size, 1 * cell_size, 1 * cell_size))

def draw_walls(cell_width, cell_height, padding_w, padding_h, maze_list, display):

    width = len(maze_list[0])
    height = len(maze_list)

    wall_width = 4 * cell_width // 5
    wall_height = 4 * cell_height // 5
    
    padded_map = np.pad(maze_list, ((1, 1), (1, 1)), mode="constant", constant_values="B")

    # Connect consecutive walls with a line
    for i in range(1,  3 + width):
        curr_x = padding_w - cell_width + i * cell_width
        for j in range(1,  3 + height):
            curr_y = padding_h - cell_height + j * cell_height
            cell = padded_map[j - 1][i - 1]

            if cell == "B":
                pygame.draw.circle(display, WALL_COLOR, (curr_x + cell_width // 2, curr_y + cell_height // 2), wall_width // 2)
                # pygame.draw.circle(self.display, RED, (curr_x + self.cell_width // 2, curr_y + self.cell_height // 2), 5)

                # Wall on top
                if j - 2 >= 0 and padded_map[j - 2][i - 1] == "B":
                    pygame.draw.rect(display, WALL_COLOR, (curr_x + cell_width // 2 - wall_width // 2, curr_y - cell_height // 2, wall_width, cell_height))
                # Wall on the left
                if i - 2 >= 0 and padded_map[j - 1][i - 2] == "B":
                    pygame.draw.rect(display, WALL_COLOR, (curr_x - cell_height // 2, curr_y + cell_height // 2 - wall_width // 2, cell_width, wall_height))

    for i in range(1,  3 + width):
        curr_x = padding_w - cell_width + i * cell_width
        for j in range(1,  3 + height):
            curr_y = padding_h - cell_height + j * cell_height
            cell = padded_map[j - 1][i - 1]

            if cell == "B":
                # Inner Wall on top
                if j - 2 >= 0 and padded_map[j - 2][i - 1] == "B":
                    pygame.draw.rect(display, BLACK, (curr_x + cell_width // 2 - wall_width // 4, curr_y - cell_height // 2, wall_width // 2, cell_height))
                # Inner Wall on the left
                if i - 2 >= 0 and padded_map[j - 1][i - 2] == "B":
                    pygame.draw.rect(display, BLACK, (curr_x - cell_width // 2, curr_y + cell_height // 2 - wall_height // 4, cell_width, wall_height // 2))

                pygame.draw.circle(display, BLACK, (curr_x + cell_width // 2, curr_y + cell_height // 2), wall_width // 4)
