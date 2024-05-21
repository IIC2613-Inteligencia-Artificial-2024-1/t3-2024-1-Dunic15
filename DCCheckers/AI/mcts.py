from math import log,sqrt,e,inf
import random
import time
from copy import deepcopy
from checkers.constants import MCTSMeta, GameMeta


class Node:
    def __init__(self, move, skip, parent, state):
        self.move = move
        self.skip = skip
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.children = {}
        self.outcome = GameMeta.PLAYERS['none']
        self.node_state = deepcopy(state)

    def add_children(self, children: dict) -> None:
        for child in children:
            self.children[child.move] = child

    def value(self, explore: float = MCTSMeta.EXPLORATION):
        if self.N == 0:
            return 0 if explore == 0 else GameMeta.INF
        else:
            return self.Q / self.N + explore * sqrt(log(self.parent.N) / self.N)

class MCTS:
    def __init__(self, state, color, over):
        self.root_state = deepcopy(state)
        self.root = Node(None, None, None, state)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0
        self.over = over
        self.color = color

    def set_turn_parameters(self, state, color, over):
        self.root_state = deepcopy(state)
        self.root = Node(None, None, None, state)
        self.color = color
        self.over = over

    def select_node(self) -> tuple:
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_value]

            node = random.choice(max_nodes)
            piece = node.move[0]
            row = node.move[1]
            col = node.move[2]

            # state.move(piece, row, col)
            state.move(piece, row, col)
            # node.move -> (piece, row, col)
            # board.move(piece, row, col)
            
            if node.N == 0:
                return node, state

        if self.expand(node, state):
            node = random.choice(list(node.children.values()))
            piece = node.move[0]
            row = node.move[1]
            col = node.move[2]

            state.move(piece, row, col)
            # state.board.move(piece, row, col)

        return node, state

    def expand(self, parent: Node, state) -> bool:
        if self.winner_mcts(state, self.color) != 0 or self.over:
            return False
        # {board: (row, col, piece, skip)}
        # pero children debe recibir (piece, row, col, skip)
        children = []
        for key, value in get_all_moves(state, self.color).items():
            nodo = Node((value[2], value[0], value[1]), value[3], parent, key)
            children.append(nodo)

        # children = [Node((move[2], move[0], move[1]), parent, state) for move in get_all_moves(state, self.color)[0]]
        parent.add_children(children)
        return True
    
    def roll_out(self, state) -> int:
        simulation_color = deepcopy(self.color)
        temp_state = deepcopy(state)
        outcome = self.winner_mcts(temp_state, simulation_color)
        i = 0
        while outcome == 0:
            i += 1
            posibles_estados = list(get_all_moves(temp_state, simulation_color).keys())
            moves = list(get_all_moves(temp_state, simulation_color).values())
            if moves == []:
                outcome = 2 if simulation_color == (255, 255, 255) else 1
                break
            next_state = random.choice(posibles_estados)
            temp_state = next_state
            simulation_color = (255, 255, 255) if simulation_color == (0, 0, 0) else (0, 0, 0)
            outcome = self.winner_mcts(temp_state, simulation_color)

        return outcome



    def back_propagate(self, node: Node, turn: int, outcome: int) -> None:
        # For the current player, not the next player
        reward = 1 if outcome == turn else 0
        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            if outcome == 0:
                reward = 0
            else:
                reward = 1 - reward


    def actualizar_root(self, new_state):
        if self.root_state is not None:
          for nodo_t in self.root.children.values():
              if nodo_t.node_state.eq(new_state):
                  self.root = nodo_t
                  self.root_state = nodo_t.node_state
                  return None
              else:
                  self.root_state = deepcopy(new_state)
                  self.root = Node(None, None, None, new_state)
        else:
            self.root_state = deepcopy(new_state)
            self.root = Node(None, None, None, new_state)

    def search(self, time_limit: int):
        
        start_time = time.process_time()
        num_rollouts = 0
        iter = 2
        i = 0
        while time.process_time() - start_time < time_limit:
        # while i < iter:
            i += 1
            # print(time.process_time() - start_time, time_limit)
            node, state = self.select_node()
            outcome = self.roll_out(state)
            to_play = 1 if self.color == (255, 255, 255) else 2
            self.back_propagate(node, to_play, outcome)
            num_rollouts += 1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

    def best_move(self):
        if self.winner_mcts(self.root_state, self.color) != 0:
            return  None

        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        best_child = random.choice(max_nodes)

        self.root_state.move(best_child.move[0], best_child.move[1], best_child.move[2])
        # console_draw(self.root_state.board)
        dict_states = get_all_moves(self.root_state, self.color)
        self.root_state = best_child.node_state
        return best_child.node_state

    def statistics(self) -> tuple:
        return self.num_rollouts, self.run_time
    
    def winner_mcts(self, state, simulation_color):
        if state.black_left <= 0:
            return 1
        elif state.white_left <= 0:
            return 2
        elif list(get_all_moves(state, simulation_color).values()) == []:
            winner = 2 if simulation_color == (255, 255, 255) else 1
            return winner
        else:
            return 0
    


# def get_all_moves(state, color):
#     board = state
#     moves = []
#     map_state_move = {}
#     for piece in board.get_all_pieces(color):
#         valid_moves = board.get_valid_moves(piece)
#         for move, skip in valid_moves.items():
#             temp_board = deepcopy(board)
#             second_board = deepcopy(board)
#             temp_piece = temp_board.get_piece(piece.row, piece.col)
#             pre_piece = second_board.get_piece(piece.row, piece.col)
#             # print("piece is moving from ", temp_piece.row, temp_piece.col, " to ", move)
#             # print("piece is moving from ", temp_piece.row, temp_piece.col, " to ", move)
#             if pre_piece == 0:
#                 continue
#             moves.append((move[0], move[1], pre_piece, skip))
#     return moves # Lista de (row, col, piece) 

def get_all_moves(board, color):
    moves = []
    map_state_move = {}

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            second_board = deepcopy(board) #*
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            pre_piece = second_board.get_piece(piece.row, piece.col) #*
            if pre_piece == 0:
                continue
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append((move[0], move[1], pre_piece, skip))
            map_state_move[new_board] = [move[0], move[1], pre_piece, skip]
    return map_state_move # Dict de {board: (row, col, piece, skip)}



def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


""" ROWS, COLS = 8, 8
WHITE = (255, 255, 255)
def move(self, piece, row, col): 
    self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
    piece.move(row, col)

    if row == ROWS - 1 or row == 0:
        piece.make_king()
        if piece.color == WHITE:
            self.white_kings += 1
        else:
            self.black_kings += 1 """

def console_draw(string_board):
    for row in string_board:
        row_str = ""
        for square in row:
            if square == 0:
                row_str += "- "
            elif square.color == (255, 255, 255):
                row_str += "B "
            elif square.color == (0, 0, 0):
                row_str += "N "

        print(row_str.strip())
