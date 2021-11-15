import random
import time

from random import randrange


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3
    n = 3
    s = 3
    b = 3
    test = 0
    depth = 0

    randomI = 0
    randomJ = 0
    randIList = []
    randJList = []

    def __init__(self, recommend=True):
        self.initialize_game()
        self.recommend = recommend

    def initialize_game(self):

        # ask for inputs
        self.n = int(input("Enter size of board (n):"))
        self.s = int(input("Enter winning line-up size(s):"))
        self.b = int(input("Enter number of blocks (b):"))

        matrix = []
        for i in range(0, self.n):
            a = []
            for j in range(0, self.n):
                a.append('.')
            matrix.append(a)

        # ask block coordinates
        for bl in range(self.b):
            self.randomI = int(input("Enter X coordinate:"))
            self.randIList.append(self.randomI)
            self.randomJ = int(input("Enter Y coordinate:"))
            self.randJList.append(self.randomJ)
            print("Coordinates you entered: (", self.randIList[bl], ", ", self.randJList[bl], ")")

        # place blocks
        for i in range(0, self.b):
            matrix[self.randIList[i]][self.randJList[i]] = "/"

        self.current_state = matrix

        # Player X always plays first
        self.player_turn = 'X'

    def draw_board(self):
        print()
        for y in range(0, self.n):
            for x in range(0, self.n):
                print(F'{self.current_state[x][y]}', end=" ")
            print()
        print()

    def is_valid(self, px, py):
        if px < 0 or px > self.n - 1 or py < 0 or py > self.n - 1:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):
        # Vertical win
        Xcounter = 0
        Ocounter = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == 'X':
                    Xcounter += 1
                    Ocounter = 0
                    continue

                if self.current_state[i][j] == '0':
                    Ocounter += 1
                    Xcounter = 0
                    continue

            if Xcounter == self.s:
                return 'X'

            if Ocounter == self.s:
                return '0'

            Xcounter = 0
            Ocounter = 0

        # Horizontal win
        Xcounter = 0
        Ocounter = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[j][i] == 'X':
                    Xcounter += 1
                    Ocounter = 0
                    continue

                if self.current_state[j][i] == '0':
                    Ocounter += 1
                    Xcounter = 0
                    continue

            if Xcounter == self.s:
                return 'X'

            if Ocounter == self.s:
                return '0'

            Xcounter = 0
            Ocounter = 0

        # Main diagonal win

        Xcounter = 0
        Ocounter = 0
        for i, j in zip(range(0, self.n), range(0, self.n)):

            if self.current_state[i][j] == 'X':
                Xcounter += 1
                Ocounter = 0

            if self.current_state[i][j] == '0':
                Ocounter += 1
                Xcounter = 0

            if Xcounter == self.s:
                return 'X'

            if Ocounter == self.s:
                return '0'

        # Second diagonal win
        Xcounter = 0
        Ocounter = 0
        for i, j in zip(range(0, self.n), range(self.n - 1, -1, -1)):

            if self.current_state[i][j] == 'X':
                Xcounter += 1
                Ocounter = 0

            if self.current_state[i][j] == '0':
                Ocounter += 1
                Xcounter = 0

            if Xcounter == self.s:
                return 'X'

            if Ocounter == self.s:
                return '0'

        # Is whole board full?

        for i in range(0, self.n):
            for j in range(0, self.n):
                # There's an empty field, we continue the game
                if (self.current_state[i][j] == '.'):
                    return None
        # It's a tie!
        return '.'

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is x!')
            elif self.result == '0':
                print('The winner is 0!')
            elif self.result == '.':
                print("It's a tie!")
            self.initialize_game()
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = '0'
        elif self.player_turn == '0':
            self.player_turn = 'X'
        return self.player_turn

    def e1(self, current_state):  # targets horizontals
        tilechecker = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if current_state[j][i] == 'X' or current_state[j][i] == '0' or current_state[j][i] == '/':
                    tilechecker -= 1
                if current_state[i][j] == '.':
                    tilechecker += 1
                    x = i
                    y = j
        for i in range(0, self.n):
            for j in range(0, self.n):
                if current_state[i][j] == 'X' or current_state[i][j] == '0' or current_state[i][j] == '/':
                    tilechecker -= 1
                if current_state[i][j] == '.':
                    tilechecker += 1
                    x = i
                    y = j

        return tilechecker, x, y

    def e2(self, current_state):  # targets diagonals
        tilechecker = 0
        x = 0
        y = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if i == j:
                    if current_state[i][j] == 'X' or current_state[i][j] == '0' or current_state[i][j] == '/':
                        tilechecker -= 1
                    if current_state[i][j] == '.':
                        tilechecker += 1
                        x = i
                        y = j

        for i, j in zip(range(0, self.n), range(self.n - 1, -1, -1)):

            if current_state[i][j] == 'X' or current_state[i][j] == '0' or current_state[i][j] == '/':
                tilechecker -= 1
            if current_state[i][j] == '.':
                tilechecker += 1
                x = i
                y = j
        if current_state[x][y] != '.':  # if diagonals are full selects 1st empty tile
            for i in range(0, self.n):
                for j in range(0, self.n):
                    if self.current_state[i][j] == '.':
                        x = i
                        y = j

        return tilechecker, x, y

    def minimax(self, depth, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()

        ''' if result or maxdepth or timer:
            return e1(self.current_state[x][y])'''

        if depth >= 3 or result:
            print('ded' + str(depth))
            return self.e2(self.current_state)

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:  # if max is true
                        self.current_state[i][j] = '0'
                        (v, _, _) = self.minimax(depth + 1, max=False)  # swap turns to min
                        self.depth += 1
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(depth + 1, max=True)  # swap turns to max
                        self.depth += 1
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'

        return (1, x, y)

    def alphabeta(self, alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = self.n - 1
        if max:
            value = -self.n - 1
        x = None
        y = None
        result = self.is_end()
        if self.depth > 100000:
            return (-1, x, y)
        if result == 'X':
            return (-1, x, y)
        elif result == '0':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = '0'
                        (v, _, _) = self.alphabeta(alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(alpha, beta, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value
        # self.test+=1
        # print(self.test)
        self.depth += 1
        return (value, x, y)

    def play(self, algo=None, player_x=None, player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(self.depth, max=False)
                else:
                    (_, x, y) = self.minimax(self.depth, max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(max=False)
                else:
                    (m, x, y) = self.alphabeta(max=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == '0' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == '0' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()


def main():
    g = Game(recommend=True)
    g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.AI)
    g.play(algo=Game.MINIMAX, player_x=Game.HUMAN, player_o=Game.HUMAN)
    g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.HUMAN)


if __name__ == "__main__":
    main()
