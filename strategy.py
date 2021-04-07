import copy
import time
import io
import random
from math import inf as infinity
from random import randint

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'


class Strategy():
    # implement all the required methods on your own
    def best_strategy(self, board, player, best_move, running):
        opp = RandomPlayer()


        if(player == BLACK):
            game = Board(player, opp, board)
        else:
            game = Board(opp, player, board)

        legal_moves = game.get_legal_moves(board)

        if player == BLACK:
            list = legal_moves[0]
        else:
            list = legal_moves[1]
        index = randint(0, len(list)-1)
        #return list[index]
        best_move.value = list[index]
        #best_move.value = self.move(game, player, legal_moves, 3)

    def move(self, board, token, legal_moves, depth):
        best_move, eval_value = self.alphabeta(board, token, legal_moves, depth)
        return best_move

    def utility(self, token, board, maximizing_player):
        game = board.board_state
        legal_moves = board.get_legal_moves(game)

        if token == BLACK:
            active_moves = legal_moves[0]
            other_moves = legal_moves[1]
            opp = WHITE
        else:
            active_moves = legal_moves[1]
            other_moves = legal_moves[0]
            opp = BLACK

        corners = [11, 18, 81, 88]
        edges = [12, 13, 14, 15, 16, 17, 21, 31, 41, 51, 61, 71, 82,
                 83, 84, 85, 86, 87, 28, 38, 48, 58, 68, 78]

        my_corners = 0
        opp_corners = 0

        my_edges = 0
        opp_edges = 0

        for index in corners:
            if game[index] == token:
                my_corners += 1
            elif game[index] == opp:
                opp_corners += 1

        for index in edges:
            if game[index] == token:
                my_edges += 1
            elif game[index] == opp:
                my_edges += 1

        my_count = 0
        opp_count = 0
        for char in board.board_state:
            if char == token:
                my_count += 1
            if char == opp:
                opp_count += 1

        my_moves = len(active_moves)
        opp_moves = len(other_moves)
        mobility_val = 0
        edges_val = 0
        corners_val = 0
        colors_count = 0
        if maximizing_player is True:
            if my_moves + opp_moves != 0:
                mobility_val = 25 * (my_moves - opp_moves)
            if (my_edges + opp_edges != 0):
                edges_val = 75 * (my_edges - opp_edges)
            if my_corners + opp_corners != 0:
                corners_val = 100 * (my_corners - opp_corners)
            colors_count = my_count - opp_count
        else:
            if my_moves + opp_moves != 0:
                mobility_val = 25 * (opp_moves - my_moves)
            if (my_edges + opp_edges != 0):
                edges_val = 75 * (opp_edges - my_edges)
            if my_corners + opp_corners != 0:
                corners_val = 100 * (opp_corners - my_corners)
            colors_count = opp_count - my_count
        return mobility_val + edges_val + corners_val + colors_count

    def alphabeta(self, board, token, legal_moves, depth=float("inf")):
        # TODO: finish this function
        best_val = 0
        best_move = None
        best_val, best_move = self.Max_Value(board, token, legal_moves, float("-inf"), float("inf"), depth)
        return best_move, best_val

    def Max_Value(self, board, token, legal_moves, alpha, beta, depth=float("inf")):

        if token == BLACK:
            active_moves = legal_moves[0]
        else:
            active_moves = legal_moves[1]

        if len(active_moves) == 0:
            return self.utility(token, board, False)

        value = float("-inf")
        best_move = active_moves[0]

        for state in active_moves:
            new_game = board.forecast_move(board.board_state, token, state)
            if depth > 0:
                new_util, new_best_move = self.Min_Value(new_game, token,
                                                         new_game.get_legal_moves(new_game.board_state),
                                                         alpha, beta, depth - 1)
                if new_util > value:
                    value = new_util
                    best_move = new_best_move
                if value > beta:
                    return value, best_move
                if value > alpha:
                    aplha = value
        return value, best_move

    def Min_Value(self, board, token, legal_moves, alpha, beta, depth=float("inf")):

        if token == BLACK:
            active_moves = legal_moves[0]
        else:
            active_moves = legal_moves[1]

        if len(active_moves) == 0:
            return self.utility(token, board, True)

        value = float("inf")
        best_move = active_moves[0]

        for state in active_moves:
            new_game = board.forecast_move(board.board_state, token, state)

            if depth > 0:
                new_util, new_best_move = self.Max_Value(new_game, token,
                                                         new_game.get_legal_moves(new_game.board_state),
                                                         alpha, beta, depth - 1)
                if new_util < value:
                    value = new_util
                    best_move = new_best_move
                if value < alpha:
                    return value, best_move
                if value < beta:
                    beta = value
        return value, best_move

class Board:

    def __init__(self, initial, player_1, player_2):

        self.player_1 = player_1
        self.player_2 = player_2
        self.token_1 = BLACK
        self.token_2 = WHITE
        self.board_state = initial

    def get_legal_moves(self, board):
        lm = [[], []]
        for index in range(11, 89):
            if board[index] == BLACK or board[index] == WHITE:
                if board[index] == BLACK:
                    opp = WHITE
                    pos = 0
                else:
                    opp = BLACK
                    pos = 1
                right = index + 1
                left = index - 1
                up = index - 10
                down = index + 10
                ru_diag = index - 9
                rd_diag = index + 11
                lu_diag = index - 11
                ld_diag = index + 9

                if board[right] == opp:
                    while board[right] == opp:
                        right = right + 1
                    if board[right] == EMPTY:
                        lm[pos].append(right)

                if board[left] == opp:
                    while board[left] == opp:
                        left = left - 1
                    if board[left] == EMPTY:
                        lm[pos].append(left)

                if board[up] == opp:
                    while board[up] == opp:
                        up = up - 10
                    if board[up] == EMPTY:
                        lm[pos].append(up)

                if board[down] == opp:
                    while board[down] == opp:
                        down = down + 10
                    if board[down] == EMPTY:
                        lm[pos].append(down)

                if board[ru_diag] == opp:
                    while board[ru_diag] == opp:
                        ru_diag = ru_diag - 9
                    if board[ru_diag] == EMPTY:
                        lm[pos].append(ru_diag)

                if board[rd_diag] == opp:
                    while board[rd_diag] == opp:
                        rd_diag = rd_diag + 11
                    if board[rd_diag] == EMPTY:
                        lm[pos].append(rd_diag)

                if board[lu_diag] == opp:
                    while board[lu_diag] == opp:
                        lu_diag = lu_diag - 11
                    if board[lu_diag] == EMPTY:
                        lm[pos].append(lu_diag)

                if board[ld_diag] == opp:
                    while board[ld_diag] == opp:
                        ld_diag = ld_diag + 9
                    if board[ld_diag] == EMPTY:
                        lm[pos].append(ld_diag)
        return lm

    def make_move(self, board, token, legal_move):
        result = board[0:legal_move] + token + board[legal_move+1:]
        board = result
        if token == BLACK:
            opp = WHITE
        else:
            opp = BLACK

        right = legal_move + 1
        if board[right] == opp:
            while board[right] == opp:
                right = right + 1
            if board[right] == token:
                right = legal_move + 1
                while board[right] == opp:
                    result = result[0:right] + token + result[right + 1:]
                    right = right + 1

        left = legal_move - 1
        if board[left] == opp:
            while board[left] == opp:
                left = left - 1
            if board[left] == token:
                left = legal_move - 1
                while board[left] == opp:
                    result = result[0:left] + token + result[left + 1:]
                    left = left - 1

        up = legal_move - 10
        if board[up] == opp:
            while board[up] == opp:
                up = up - 10
            if board[up] == token:
                up = legal_move - 10
                while board[up] == opp:
                    result = result[0:up] + token + result[up + 1:]
                    up = up - 10

        down = legal_move + 10
        if board[down] == opp:
            while board[down] == opp:
                down = down + 10
            if board[down] == token:
                down = legal_move + 10
                while board[down] == opp:
                    result = result[0:down] + token + result[down + 1:]
                    down = down + 10

        ru_diag = legal_move - 9
        if board[ru_diag] == opp:
            while board[ru_diag] == opp:
                ru_diag = ru_diag - 9
            if board[ru_diag] == token:
                ru_diag = legal_move - 9
                while board[ru_diag] == opp:
                    result = result[0:ru_diag] + token + result[ru_diag + 1:]
                    ru_diag = ru_diag - 9

        rd_diag = legal_move + 11
        if board[rd_diag] == opp:
            while board[rd_diag] == opp:
                rd_diag = rd_diag + 11
            if board[rd_diag] == token:
                rd_diag = legal_move + 11
                while board[rd_diag] == opp:
                    result = result[0:rd_diag] + token + result[rd_diag + 1:]
                    rd_diag = rd_diag + 11

        lu_diag = legal_move - 11
        if board[lu_diag] == opp:
            while board[lu_diag] == opp:
                lu_diag = lu_diag - 11
            if board[lu_diag] == token:
                lu_diag = legal_move - 11
                while board[lu_diag] == opp:
                    result = result[0:lu_diag] + token + result[lu_diag + 1:]
                    lu_diag = lu_diag - 11

        ld_diag = legal_move + 9
        if board[ld_diag] == opp:
            while board[ld_diag] == opp:
                ld_diag = ld_diag + 9
            if board[ld_diag] == token:
                ld_diag = legal_move + 9
                while board[ld_diag] == opp:
                    result = result[0:ld_diag] + token + result[ld_diag + 1:]
                    ld_diag = ld_diag + 9

        result = result[0:legal_move] + token + result[legal_move + 1:]
        return result

    def forecast_move(self, board, token, legal_move):
        new_board = copy.deepcopy(self)
        new_board.make_move(board, token, legal_move)
        return new_board

    def copy(self):
        b = Board(self.board_state, self.player_1, self.player_2)
        b.token_1 = BLACK
        b.token_2 = WHITE
        b.board_state = self.board_state
        return b

class RandomPlayer():
    """Player that chooses a move randomly."""
    __name__ = ""

    def move(self, board, token, legal_moves):
        if token == BLACK:
            list = legal_moves[0]
        else:
            list = legal_moves[1]
        index = randint(0, len(list)-1)
        return list[index]

