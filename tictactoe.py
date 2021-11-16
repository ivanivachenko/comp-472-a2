import random
import time
import wsgiref.validate

from random import randrange


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3
    n = 3
    s = 3
    b = 3
    t = 0   #max time allowed
    test = 0
    d1 = 0
    d2 = 0
    a1 = MINIMAX
    a2 = MINIMAX
    #e = True   #euristic
    e1 = 1
    e2 = 2
    player_x = AI
    player_o = AI

    randomI = 0
    randomJ = 0
    randIList = []
    randJList = []
    fileName = ""

    #for file outputs
    total_nb_states = 0
    all_ev_times = []
    average_ev_time = 0
    total_nb_moves = 0
    nb_states_current_move = 0

    def __init__(self, recommend=True):
        self.initialize_game()
        self.recommend = recommend

    def initialize_game(self):

        # ask for inputs
        self.n = int(input("Enter size of board (n):"))
        self.s = int(input("Enter winning line-up size(s):"))
        self.b = int(input("Enter number of blocks (b):"))

        self.t = int(input("Enter the maximum time to return a move (in seconds) (t):"))

        self.e1 = int(input("Chose the euristic to use (e) - 1 or 2:"))
        self.e2 = int(input("Chose the euristic to use (e) - 1 or 2:"))

        self.a1 = int(input("Chose between MINIMAX (0) or ALPHABETA (1):"))
        self.a2 = int(input("Chose between MINIMAX (0) or ALPHABETA (1):"))
        self.d1 = int(input("Enter maximum depth of AI 1:"))
        self.d2 = int(input("Enter maximum depth of AI 2:"))

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

        self.fileName = "gameTrace-" + str(self.n) + str(self.b) + str(self.s) + str(self.t) + ".txt"
        self.writegametracefiles()

    def writegametracefiles(self):
        with open(self.fileName, 'w') as f:
            f.write("This is a game trace file")
            f.write("\n\nParameters of the game:")
            f.write("\nn = " + str(self.n))
            f.write("\nb = " + str(self.b))
            f.write("\ns = " + str(self.s))
            f.write("\nt = " + str(self.t))

            f.write("\n\nPosition of the blocks:\n")
            if self.b != 0:
                for b in range(0, self.b):
                    f.write("(" + str(self.randIList[b]) + ", " + str(self.randJList[b]) + ")")
            else:
                f.write("There are no blocks in this game.")

            f.write("\n\nParameters of each player:\n")
            if Game.player_x == 3:
                f.write("AI")
            else:
                f.write("HUMAN")
            f.write(" vs ")
            if Game.player_o == 3:
                f.write("AI")
            else:
                f.write("HUMAN")

            if Game.player_x == 3:
                f.write("\n\nPlayer X:")
                f.write("\nMaximum depth = " + str(self.d1))
                f.write("\nEuristic = " + str(self.e1))
                f.write("\nMinimax (0) or Alphabeta (1) = " + str(self.a1))
            if Game.player_o == 3:
                f.write("\n\nPlayer O:")
                f.write("\nMaximum depth = " + str(self.d2))
                f.write("\nEuristic = " + str(self.e2))
                f.write("\nMinimax (0) or Alphabeta (1) = " + str(self.a2))

            f.write("\n\nInitial configuration of the board:")
            self.draw_board()
            f.close()

    def draw_board(self):
        print()
        for y in range(0, self.n):
            for x in range(0, self.n):
                print(F'{self.current_state[x][y]}', end=" ")
            print()
        print()

        with open(self.fileName, 'a') as f:
            f.write("\n")
            for y in range(0, self.n):
                for x in range(0, self.n):
                    f.write(F'{self.current_state[x][y]}')
                f.write("\n")
            f.write("\n")

    def write_move_stats(self, pX, pO, start, end, x, y):
        with open(self.fileName, 'a') as f:
            #f.write("Nb of states evaluated: " + str(nbS))
            if (self.player_turn == 'X' and pX == self.HUMAN) or (
                    self.player_turn == '0' and pO == self.HUMAN):
                if self.recommend:
                    f.write("\n" + F'Evaluation time: {round(end - start, 7)}s')
                    f.write("\n" + F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and pX == self.AI) or (self.player_turn == '0' and pO == self.AI):
                f.write("\n" + F'Evaluation time: {round(end - start, 7)}s')
                f.write("\n" + F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            f.close()

    def write_end_game(self):
        with open(self.fileName, 'a') as f:
            #6.a
            if self.result != None:
                if self.result == 'X':
                    f.write('The winner is x!')
                elif self.result == '0':
                    f.write('The winner is 0!')
                elif self.result == '.':
                    f.write("It's a tie!")

            #6.b.i
            for t in self.all_ev_times:
                self.average_ev_time += t
            self.average_ev_time = self.average_ev_time / self.all_ev_times.__sizeof__()
            f.write("\nAverage evaluation time of the heuristic for each state evaluated: " + str(self.average_ev_time))

            #6.b.ii
            f.write("\nTotal number of states evaluated during the game: " + str(self.total_nb_states))

            #6.b.iii
            f.write("\nAverage of per-move average depth")

            #6.b.vi
            f.write("\nTotal number of moves in the game: " + str(self.total_nb_moves))



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
            self.write_end_game()
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

    #happens for 1 state
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

        self.nb_states_current_move += 1
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

    def minimax(self, depth, e, max=False):
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


        if (depth >= 3 or result) and e == 1:
            return self.e1(self.current_state)

        if (depth >= 3 or result) and e == 2:
            return self.e2(self.current_state)

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    self.total_nb_states += 1
                    if max:  # if max is true
                        self.current_state[i][j] = '0'
                        #for 1 depth
                        (v, _, _) = self.minimax(depth + 1, e, max=False)  # swap turns to min
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        #for 1 depth
                        (v, _, _) = self.minimax(depth + 1, e, max=True)  # swap turns to max
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'

        self.nb_states_current_move += 1
        return 1, x, y

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
        if result == 'X':
            return (-1, x, y)
        elif result == '0':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    self.total_nb_states += 1
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
        return (value, x, y)

    def play(self, algo=None, player_x=None, player_o=None):
        #global nbs
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board() #new configuration of the board
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(self.d1, self.e1, max=False)
                else:
                    (_, x, y) = self.minimax(self.d2, self.e2, max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(max=False)
                else:
                    (m, x, y) = self.alphabeta(max=True)
            end = time.time()
            self.write_move_stats(player_x, player_o, start, end, x, y)
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == '0' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    self.all_ev_times.append(round(end - start, 7))
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == '0' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                self.all_ev_times.append(round(end - start, 7))
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}') #move taken
            self.current_state[x][y] = self.player_turn
            self.switch_player()

            #54.c.ii
            with open(self.fileName, 'a') as f:
                f.write("\nStates for this move: " + str(self.nb_states_current_move))
                f.close()
            self.total_nb_moves += 1





def main():
    g = Game(recommend=True)
    r = 10
    for i in range(0, r):
        g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.AI)

    g.play(algo=Game.MINIMAX, player_x=Game.HUMAN, player_o=Game.HUMAN)
    g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.HUMAN)


if __name__ == "__main__":
    main()