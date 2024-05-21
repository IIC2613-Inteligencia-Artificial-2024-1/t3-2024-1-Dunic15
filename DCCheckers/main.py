import os
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK, MONTECARLO, MINIMAX, HUMAN
from checkers.game import Game
from AI.minimax import minimax
from AI.mcts import MCTS
import time
FPS = 60

CURRENT_DIR = os.path.dirname(__file__)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    
    # Puedes determinar si los jugadores son controlados por la IA o por humanos, 
    # asignándoles MONTECARLO, MINIMAX o HUMAN.
    white_algorithm = MONTECARLO
    black_algorithm = HUMAN
    
    # Puedes elegir si quieres que MINIMAX muestre los movimientos
    # que evalua en cada jugada cambiando la siguiente variable a True
    show_moves_minimax = False

    # Profundidad de busqueda para Minimax en las fichas blancas y negras
    white_depth = 2
    black_depth = 2

    # Puedes cambiar la velocidad de la animación cambiando el valor de wait_time (milisegundos)
    wait_time = 0

    # Activar alphabeta pruning 
    # (Cambia esta variable a True cuando lo hayas implementado)
    alphabeta = False

    game = Game(WIN, show_moves_minimax, wait_time)
    new_board = game.board

    # Variables para calcular el tiempo promedio de búsqueda
    total_white_search_time = 0
    total_black_search_time = 0
    num_white_searches = 0
    num_black_searches = 0


    MONTE_CARLO_THINK_TIME = 2

    while run:
        clock.tick(FPS)
        
        if game.turn == WHITE and white_algorithm != HUMAN:
            start_time = time.time()

            if white_algorithm == MINIMAX:
                value, new_board = minimax(game.get_board(), white_depth, WHITE, BLACK, game, alphabeta)

            elif white_algorithm == MONTECARLO: 
                over = True if game.winner() else False
                MonteCarlo = MCTS(game.get_board(), WHITE, over)
                MonteCarlo.search(MONTE_CARLO_THINK_TIME)
                num_rollouts, run_time = MonteCarlo.statistics()
                print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
                move = MonteCarlo.best_move()
                new_board = move

            if new_board is not None:
                game.ai_move(new_board)
                total_white_search_time += time.time() - start_time
                num_white_searches += 1
        
        elif game.turn == BLACK and black_algorithm != HUMAN:
            start_time = time.time()

            if black_algorithm == MINIMAX:
                value, new_board = minimax(game.get_board(), black_depth, BLACK, WHITE, game, alphabeta)

            elif black_algorithm == MONTECARLO: 
                over = True if game.winner() else False
                MonteCarlo = MCTS(game.get_board(), BLACK, over)
                MonteCarlo.search(MONTE_CARLO_THINK_TIME)
                num_rollouts, run_time = MonteCarlo.statistics()
                print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
                move = MonteCarlo.best_move()
                new_board = move



            if new_board is not None:
                game.ai_move(new_board)
                total_black_search_time += time.time() - start_time
                num_black_searches += 1
            

        if game.winner() is not None:
            if game.winner() == BLACK:
                print(f"BLACK {black_algorithm} WINS")
            else:
                print(f"WHITE {white_algorithm} WINS")
            run = False


        if new_board is None:
            if game.turn == BLACK:
                print(f"WHITE {white_algorithm} WINS")
            elif game.turn == WHITE:
                print(f"BLACK {black_algorithm} WINS")

            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
                # piece = game.piece_selected()

                # if not game.select(row, col):
                #   move = (row, col)
                #   print(piece.piece_coordinates(), move)

        game.update()
    
    pygame.quit()

    if num_white_searches > 0:
        average_white_search_time = total_white_search_time / num_white_searches
        print(f"Tiempo promedio de búsqueda por movimiento WHITE ({white_algorithm}): {average_white_search_time:.6f} segundos")
        #print(f"Tiempo total de búsqueda WHITE ({white_algorithm}): {total_white_search_time:.6f} segundos")
    if num_black_searches > 0:
        average_black_search_time = total_black_search_time / num_black_searches
        print(f"Tiempo promedio de búsqueda por movimiento BLACK ({black_algorithm}): {average_black_search_time:.6f} segundos")
        #print(f"Tiempo total de búsqueda BLACK ({black_algorithm}): {total_black_search_time:.6f} segundos")

main()
