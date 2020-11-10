import random
from enum import IntEnum, Enum
import copy


class Game:
    class __PositionValuesEnum(IntEnum):
        WHITE = 0
        PLAYER_1 = 1
        PLAYER_2 = 2

    class __PawnMoves(Enum):
        UP = (1, 0)
        UPRIGHT = (1, 1)
        RIGHT = (0, 1)
        DOWNRIGHT = (-1, 1)
        DOWN = (-1, 0)
        DOWNLEFT = (-1, -1)
        LEFT = (0, -1)
        UPLEFT = (1, -1)

    def __init__(self):
        self.__board = [
            [position_value for i in range(4)]
            for position_value in (
                Game.__PositionValuesEnum.PLAYER_1,
                Game.__PositionValuesEnum.WHITE,
                Game.__PositionValuesEnum.WHITE,
                Game.__PositionValuesEnum.PLAYER_2
            )
        ]

        self.__board_labels_x = ['A', 'B', 'C', 'D']
        self.__board_labels_y = ['1', '2', '3', '4']

    def print_board(self):
        print()

        for i in reversed(range(4)):
            print(self.__board_labels_y[i], end='    ')
            for j in range(4):
                print(int(self.__board[i][j]), end=' ')
            print()
        print()

        print(end='     ')
        for board_label_x in self.__board_labels_x:
            print(board_label_x, end=' ')
        print()

    def get_pawn_possible_moves(self, is_user_turn, pawn_position):
        allowed_pawn_value = \
            Game.__PositionValuesEnum.PLAYER_1 if is_user_turn else Game.__PositionValuesEnum.PLAYER_2

        if not self.__board[pawn_position[0]][pawn_position[1]] == allowed_pawn_value:
            return None

        return [pawn_move.name for pawn_move in Game.__PawnMoves if self.__can_perform_move(pawn_position, pawn_move)]

    def perform_move(self, is_user_turn, pawn_position, pawn_move):
        if is_user_turn and self.__board[pawn_position[0]][pawn_position[1]] != Game.__PositionValuesEnum.PLAYER_1:
            return None
        if not is_user_turn and self.__board[pawn_position[0]][pawn_position[1]] != Game.__PositionValuesEnum.PLAYER_2:
            return None
        if not self.__can_perform_move(pawn_position, pawn_move):
            return None

        self.__board[pawn_position[0]][pawn_position[1]] = Game.__PositionValuesEnum.WHITE
        self.__board[pawn_position[0] + pawn_move.value[0]][pawn_position[1] + pawn_move.value[1]] = \
            Game.__PositionValuesEnum.PLAYER_1 if is_user_turn else Game.__PositionValuesEnum.PLAYER_2

    def is_final_state(self, board=None):
        if board is None:
            board = self.__board
        player1_won = True
        player2_won = True
        for i in range(4):
            if board[0][i] != Game.__PositionValuesEnum.PLAYER_2:
                player2_won = False
            if board[3][i] != Game.__PositionValuesEnum.PLAYER_1:
                player1_won = False

        if player1_won:
            return 1
        if player2_won:
            return 2
        return False

    def get_pawn_position_from_board_labels(self, board_labels):
        return ord(board_labels[1]) - ord('1'), ord(board_labels[0]) - ord('A')

    def str_to_pawn_move(self, pawn_move_str):
        return Game.__PawnMoves[pawn_move_str]

    def __can_perform_move(self, pawn_position, pawn_move, board=None):
        if board is None:
            board = self.__board
        future_pawn_position = (pawn_position[0] + pawn_move.value[0], pawn_position[1] + pawn_move.value[1])
        return (
                future_pawn_position[0] in range(4) and future_pawn_position[1] in range(4) and
                board[future_pawn_position[0]][future_pawn_position[1]] == Game.__PositionValuesEnum.WHITE
        )

    def __heuristic(self, board, is_maximizing):
        score = 0
        for i in range(4):
            for j in range(4):
                if board[i][j] == Game.__PositionValuesEnum.PLAYER_2:
                    score += 4 - i
                elif board[i][j] == Game.__PositionValuesEnum.PLAYER_1:
                    score -= i

        return score if is_maximizing else -score

    def __minimax(self, board, pawn_position, pawn_move, depth, is_maximizing):
        if depth == 0 or self.is_final_state(board):
            return self.__heuristic(board, is_maximizing)

        board[pawn_position[0]][pawn_position[1]] = Game.__PositionValuesEnum.WHITE
        board[pawn_position[0] + pawn_move.value[0]][pawn_position[1] + pawn_move.value[1]] = \
            Game.__PositionValuesEnum.PLAYER_2 if is_maximizing else Game.__PositionValuesEnum.PLAYER_1

        pawn_positions = [
            (i, j) for i in range(4) for j in range(4)
            if board[i][j] == (Game.__PositionValuesEnum.PLAYER_2 if is_maximizing else Game.__PositionValuesEnum.PLAYER_1)
        ]

        minimax_output = [
            self.__minimax(board, pawn_position, pawn_move, depth - 1, not is_maximizing)
            for pawn_position in sorted(pawn_positions, key=lambda x: random.random())
            for pawn_move in
            sorted([pawn_move for pawn_move in Game.__PawnMoves if self.__can_perform_move(pawn_position, pawn_move, board)], key=lambda x: random.random())
        ]

        if is_maximizing:
            return max(minimax_output)

        return min(minimax_output)

    def perform_minimax(self):
        board = copy.deepcopy(self.__board)

        pawn_positions = [(i, j) for i in range(4) for j in range(4) if
                          board[i][j] == Game.__PositionValuesEnum.PLAYER_2]

        minimax_output = [
            (
                self.__minimax(board, pawn_position, pawn_move, 7, True),
                pawn_position,
                pawn_move
            )
            for pawn_position in pawn_positions
            for pawn_move in
            [pawn_move for pawn_move in Game.__PawnMoves if self.__can_perform_move(pawn_position, pawn_move, board)]
        ]

        max_output = max(minimax_output, key=lambda item: item[0])
        minimax_output = [minimax_output_instance for minimax_output_instance in minimax_output if
                          minimax_output_instance[0] == max_output[0]]

        return random.choice(minimax_output)


if __name__ == '__main__':
    game = Game()
    user_turn = True
    winner = False

    while not winner:
        game.print_board()

        if user_turn:
            pawn_choice = input('Select a pawn ([A-B][1-4]): ')
            pawn_position = game.get_pawn_position_from_board_labels(pawn_choice)

            pawn_possible_moves = game.get_pawn_possible_moves(True, pawn_position)
            if pawn_possible_moves is None:
                print('Not a/Not your pawn!')
                continue

            pawn_move_choice = input('Select which direction you want to move the pawn: (' + \
                                     '/'.join(pawn_possible_moves) + '): ').upper()
            pawn_move = game.str_to_pawn_move(pawn_move_choice)

            game.perform_move(True, pawn_position, pawn_move)
        else:
            minimax_output = game.perform_minimax()
            print(minimax_output[0])

            game.perform_move(False, minimax_output[1], minimax_output[2])

        user_turn = not user_turn
        winner = game.is_final_state()

    game.print_board()
    print('Player ' + str(winner) + ' won!')
