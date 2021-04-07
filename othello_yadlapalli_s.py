import copy
import time
import io
from random import randint
from math import inf as infinity

BLACK = 'X'
WHITE = 'O'
BLANK = '.'
WALL = '#'

# Sreya Yadlapalli 12/14/18


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
                    if board[right] == BLANK:
                        lm[pos].append(right)

                if board[left] == opp:
                    while board[left] == opp:
                        left = left - 1
                    if board[left] == BLANK:
                        lm[pos].append(left)

                if board[up] == opp:
                    while board[up] == opp:
                        up = up - 10
                    if board[up] == BLANK:
                        lm[pos].append(up)

                if board[down] == opp:
                    while board[down] == opp:
                        down = down + 10
                    if board[down] == BLANK:
                        lm[pos].append(down)

                if board[ru_diag] == opp:
                    while board[ru_diag] == opp:
                        ru_diag = ru_diag - 9
                    if board[ru_diag] == BLANK:
                        lm[pos].append(ru_diag)

                if board[rd_diag] == opp:
                    while board[rd_diag] == opp:
                        rd_diag = rd_diag + 11
                    if board[rd_diag] == BLANK:
                        lm[pos].append(rd_diag)

                if board[lu_diag] == opp:
                    while board[lu_diag] == opp:
                        lu_diag = lu_diag - 11
                    if board[lu_diag] == BLANK:
                        lm[pos].append(lu_diag)

                if board[ld_diag] == opp:
                    while board[ld_diag] == opp:
                        ld_diag = ld_diag + 9
                    if board[ld_diag] == BLANK:
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

    def play_othello(self, game):
        self.board_state = game
        mover = self.player_2
        token = WHITE
        lm = self.get_legal_moves(self.board_state)
        while len(lm[0]) != 0 or len(lm[1]) != 0:
            if len(lm[0]) != 0 and len(lm[1]) != 0:
                if mover == self.player_1:
                    mover = self.player_2
                    token = WHITE
                else:
                    mover = self.player_1
                    token = BLACK
            elif len(lm[0]) != 0:
                mover = self.player_1
                token = BLACK
            elif len(lm[1]) != 0:
                mover = self.player_2
                token = WHITE
            else:
                return
            print(token + " turn")
            move = mover.move(self, token, lm)
            self.board_state = self.make_move(self.board_state, token, move)
            self.print_state(self.board_state)
            lm = self.get_legal_moves(self.board_state)

    def print_winner(self):
        countX = 0
        countO = 0
        for char in self.board_state:
            if char == BLACK:
                countX += 1
            if char == WHITE:
                countO += 1
        print("The number of " + BLACK + " is " + str(countX))
        print("The number of " + WHITE + " is " + str(countO))

        if countX > countO:
            print("The winner is " + BLACK)
            return BLACK
        else:
            print("The winner is " + WHITE)
            return WHITE

    def print_state(self, game):
        count = 0
        for char in game:
            if char != WALL:
                print(char, end = " ")
                count += 1
            if count == 8:
                print()
                count = 0
        print()


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


class HumanPlayer():
    """Player that a human can choose a move for."""
    __name__ = ""

    def move(self, board, token, legal_moves):
        if token == BLACK:
            list = legal_moves[0]
        else:
            list = legal_moves[1]
        dict = self.create_dict(list)
        for key in dict:
            val = str(dict[key])
            print(str(key) + "(" + val[1] + ", " + val[0] + ")")
        index = input("Choose one of the moves by entering the number in front of it: ")
        return dict[int(index)]

    def create_dict(self, moves):
        dict = {}
        for i in range(0, len(moves)):
            dict[i] = moves[i]
        return dict


class MinMaxPlayer():
    """Player that uses minimax to choose a move."""
    __name__ = ""

    def __init__(self, search_depth=2):
        self.search_depth = search_depth

    def move(self, board, token, legal_moves):
        best_move, eval_value = self.minimax(board, token, legal_moves, depth=self.search_depth)
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

    def minimax(self, board, token, legal_moves, depth=float("inf")):
        # TODO: finish this function
        best_val = 0
        best_move = None
        best_val, best_move = self.Max_Value(board, token, legal_moves, depth)
        return best_move, best_val

    def Max_Value(self, board, token, legal_moves, depth=float("inf")):

        if (token == WHITE):
            opp = BLACK
            active_moves = legal_moves[1]
        else:
            opp = WHITE
            active_moves = legal_moves[0]

        if len(active_moves) == 0:
            return float("-inf"), (-1, -1)

        util, best_move = float("-inf"), active_moves[0]
        for state in active_moves:
            new_game = board.forecast_move(board.board_state, token, state)

            if depth > 0:
                new_util, new_best_move = self.Min_Value(new_game, opp,
                                                         new_game.get_legal_moves(new_game.board_state),
                                                         depth - 1)
                if new_util > util:
                    util, best_move = new_util, state
            else:
                new_util = self.utility(token, new_game, False)
                if new_util > util:
                    util, best_move = new_util, state
        return util, best_move

    def Min_Value(self, board, token, legal_moves, depth=float("inf")):

        if (token == WHITE):
            opp = BLACK
            active_moves = legal_moves[1]
        else:
            opp = WHITE
            active_moves = legal_moves[0]

        if len(active_moves) == 0:
            return float("inf"), (-1, -1)

        util, best_move = float("inf"), active_moves[0]
        for state in active_moves:
            new_game = board.forecast_move(board.board_state, token, state)

            if depth > 0:
                new_util, new_best_move = self.Max_Value(new_game, opp,
                                                         new_game.get_legal_moves(new_game.board_state),
                                                         depth - 1)
                if new_util < util:
                    util, best_move = new_util, state
            else:
                new_util = self.utility(token, new_game, True)
                if new_util < util:
                    util, best_move = new_util, state
        return util, best_move


class AlphaBetaPlayer():
    """Player that uses minimax to choose a move."""
    __name__ = ""

    def __init__(self, search_depth=3):
        self.search_depth = search_depth

    def move(self, board, token, legal_moves):
        best_move, eval_value = self.alphabeta(board, token, legal_moves, depth=self.search_depth)
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


def main():
    #initial = input("Enter the starting state(64-char string): ")
    #type1 = input("Enter the first player(human, random, minimax, alphabeta): ")
    #type2 = input("Enter the first player(human, random, minimax, alphabeta): ")
    blank = True
    for i in range(100):
        initial = ""
        type1 = "alphabeta"
        type2 = "random"
        if initial == "":
            initial = '.' * 64
        game = "###########" + initial[0:8] + "##" + initial[8:16] + "##" + initial[16: 24] + "##" + \
            initial[24: 32] + "##" + initial[32:40] + "##" + initial[40:48] + "##" + initial[48:56] + \
            "##" + initial[56: 64] + "###########"
        if blank:
            game = game[0:44] + "O" + "X" + game[46:54] + "X" + "O" \
                + game[56:]
        player_1 = RandomPlayer()
        player_2 = RandomPlayer()

        if type1 == "random":
            player_1 = RandomPlayer()
        elif type1 == "human":
            player_1 = HumanPlayer()
        elif type1 == "minimax":
            player_1 = MinMaxPlayer()
        elif type1 == "alphabeta":
            player_1 = AlphaBetaPlayer()

        if type2 == "random":
            player_2 = RandomPlayer()
        elif type2 == "human":
            player_2 = HumanPlayer()
        elif type2 == "minimax":
            player_2 = MinMaxPlayer()
        elif type2 == "alphabeta":
            player_2 = AlphaBetaPlayer()
        player_1.__name__ = "Dumbo1"
        player_2.__name__ = "Dumbo2"

        board = Board(game, player_1, player_2)
        board.print_state(game)
        board.play_othello(game)
        winner = board.print_winner()

if __name__ == '__main__':
    main()

