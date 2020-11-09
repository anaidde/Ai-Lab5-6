class Game:
    class PlaceStateEnum:
        green = 1
        red = 2
        white = 0

    class DirectionStateEnum:
        up = 1
        down = 2
        left = 3
        right = 4

    def __init__(self):
        self.board = [[Game.PlaceStateEnum.green, Game.PlaceStateEnum.green, Game.PlaceStateEnum.green,
                       Game.PlaceStateEnum.green],
                      [Game.PlaceStateEnum.white, Game.PlaceStateEnum.white, Game.PlaceStateEnum.white,
                       Game.PlaceStateEnum.white],
                      [Game.PlaceStateEnum.white, Game.PlaceStateEnum.white, Game.PlaceStateEnum.white,
                       Game.PlaceStateEnum.white],
                      [Game.PlaceStateEnum.red, Game.PlaceStateEnum.red, Game.PlaceStateEnum.red,
                       Game.PlaceStateEnum.red]]

    def is_final_state(self):
        if Game.PlaceStateEnum.white in self.board[0] and Game.PlaceStateEnum.white in self.board[3]:
            return False

        if Game.PlaceStateEnum.green in self.board[0]:
            return False

        if Game.PlaceStateEnum.red in self.board[3]:
            return False

        return True

    def movement(self, player1, pawn_position, direction):
        if not pawn_position[0] in range(4) or not pawn_position[1] in range(4):
            return False
        if player1:
            if not self.board[pawn_position[0]][pawn_position[1]] == Game.PlaceStateEnum.green:
                return False
        else:
            if not self.board[pawn_position[0]][pawn_position[1]] == Game.PlaceStateEnum.red:
                return False

        previous_pawn_position = pawn_position

        if direction == Game.DirectionStateEnum.up:
            pawn_position = (pawn_position[0] - 1, pawn_position[1])
        elif direction == Game.DirectionStateEnum.down:
            pawn_position = (pawn_position[0] + 1, pawn_position[1])
        elif direction == Game.DirectionStateEnum.left:
            pawn_position = (pawn_position[0], pawn_position[1] - 1)
        else:
            pawn_position = (pawn_position[0], pawn_position[1] + 1)

        if self.__is_valid_state(pawn_position):
            self.board[pawn_position[0]][pawn_position[1]] = Game.PlaceStateEnum.green if player1 else Game.PlaceStateEnum.red
            self.board[previous_pawn_position[0]][previous_pawn_position[1]] = Game.PlaceStateEnum.white
            return True
        return False

    def __is_valid_state(self, pawn_position): # functia de validare a starilor
        if pawn_position[0] < 0 or pawn_position[0] > 3:
            return False
        if pawn_position[1] < 0 or pawn_position[1] > 3:
            return False

        if self.board[pawn_position[0]][pawn_position[1]] != Game.PlaceStateEnum.white:
            return False

        return True

    def __get_possible_movement(self, pawn_position, player1): # Euristica
        up = self.movement(player1, pawn_position, Game.DirectionStateEnum.up)
        down = self.movement(player1, pawn_position, Game.DirectionStateEnum.down)
        left = self.movement(player1, pawn_position, Game.DirectionStateEnum.left)
        right = self.movement(player1, pawn_position, Game.DirectionStateEnum.right)

        up_score = None if up is None else 1 if player1 else -1
        down_score = None if down is None else -1 if player1 else 1
        left_score = 0 if left is not None else None
        right_score = 0 if right is not None else None

        return ((Game.DirectionStateEnum.up, up_score),
                (Game.DirectionStateEnum.down, down_score),
                (Game.DirectionStateEnum.left, left_score),
                (Game.DirectionStateEnum.right, right_score))

    def interface(self):
        for raw in self.board:
            for element in raw:
                print(element, end=' ')
            print()


game = Game()

player_1 = True
game_running = True

while game_running:
    game.interface()
    print("Is player1's turn") if player_1 else print("Is player2's turn")
    print("Choose pawn: ")
    pawn_chosen_x = int(input())
    pawn_chosen_y = int(input())
    print("Choose a direction to move: ")
    direction_chosen = input()
    if direction_chosen == "up":
        direction_chosen = Game.DirectionStateEnum.up
    elif direction_chosen == "down":
        direction_chosen = Game.DirectionStateEnum.down
    elif direction_chosen == "left":
        direction_chosen = Game.DirectionStateEnum.left
    elif direction_chosen == "right":
        direction_chosen = Game.DirectionStateEnum.right
    else:
        print("Incorrect choice!")
        continue
    pawn_chosen = (pawn_chosen_x, pawn_chosen_y)
    if not game.movement(player_1, pawn_chosen, direction_chosen):
        print("Impossible move!")
        continue
    if game.is_final_state():
        print("Player1 is the winner") if player_1 else print("Player2's is the winner")
        game_running = False
        continue

    player_1 = not player_1

game.interface()
