import os
import pygame
import math


CURRENT_DIR = os.path.dirname(__file__)

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
BROWN = (168, 121, 51)
LIGHT_BROWN = (250, 221, 144)
GREEN = (0, 255, 0)

CROWN = pygame.transform.scale(pygame.image.load(f'{CURRENT_DIR}/../assets/crown.png'), (44, 25))

MONTECARLO = "montecarlo"
MINIMAX = "minimax"
HUMAN = "human"

class GameMeta:
    PLAYERS = {'none': 0, 'white': 1, 'black': 2}
    OUTCOMES = {'none': 0, 'white': 1, 'black': 2, 'draw': 3}
    INF = float('inf')
    ROWS = 6
    COLS = 7


class MCTSMeta:
    EXPLORATION = math.sqrt(2)