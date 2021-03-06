import random
import time
import wsgiref.validate

from random import randrange


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3
    game_nb = 0
    n = 3
    s = 3
    b = 3
    t = 5   #max time allowed
    test = 0
    d1 = 0
    d2 = 0
    depth = 0
    E1 = 1
    E2 = 2
    a1 = 1
    a2 = 2
    a = True
    player_x = AI
    player_o = AI


    e1win = 0
    e2win = 0



    randomI = 0
    randomJ = 0
    randIList = []
    randJList = []
    fileName = ""

    scoreboard_activated = True

    #for file outputs
    total_nb_states = 0
    all_ev_times = []
    average_ev_time = 0
    total_nb_moves = 0
    nb_states_current_move = 0

    sb_ev_time = []
    sb_total_nb_states = []
    sb_total_nb_moves = []

    sb_av_ev_time = 0
    sb_av_nb_states = 0
    sb_av_nb_moves = 0

    def __init__(self, recommend=True):
        self.initialize_game()
        self.recommend = recommend

    def initialize_game(self):

        if self.scoreboard_activated is False:
            # ask for inputs
            self.n = int(input("Enter size of board (n):"))
            self.s = int(input("Enter winning line-up size(s):"))
            self.b = int(input("Enter number of blocks (b):"))

            self.t = int(input("Enter the maximum time to return a move (in seconds) (t):"))

            self.E1 = int(input("Chose the euristic to use (e) - 1 or 2:"))
            self.E2 = int(input("Chose the euristic to use (e) - 1 or 2:"))

            #self.a1 = int(input("Chose between MINIMAX (0) or ALPHABETA (1):"))
            #self.a2 = int(input("Chose between MINIMAX (0) or ALPHABETA (1):"))

            self.d1 = int(input("Enter maximum depth of AI 1:"))
            self.d2 = int(input("Enter maximum depth of AI 2:"))

        else:
            #set default inputs
            self.n = 5
            self.s = 4
            self.b = 0
            self.t = 0
            self.E1 = 1
            self.E2 = 2
            self.d1 = 3
            self.d2 = 4

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
                f.write("\nEuristic = " + str(self.E1))
                f.write("\nMinimax (0) or Alphabeta (1) = " + str(self.a1))
            if Game.player_o == 3:
                f.write("\n\nPlayer O:")
                f.write("\nMaximum depth = " + str(self.d2))
                f.write("\nEuristic = " + str(self.E2))
                f.write("\nMinimax (0) or Alphabeta (1) = " + str(self.a2))

            f.write("\n\nInitial configuration of the board:")
            self.draw_board()
            f.close()

    def writescoreboard(self):
        with open("scoreboard.txt", 'a') as f:
            f.write("SCOREBOARD")
            f.write("\n\nParameters of the game:")
            f.write("\nn = " + str(self.n))
            f.write("\nb = " + str(self.b))
            f.write("\ns = " + str(self.s))
            f.write("\nt = " + str(self.t))

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
                f.write("\nEuristic = " + str(self.E1))
                f.write("\nMinimax (0) or Alphabeta (1) = " + str(self.a1))
            if Game.player_o == 3:
                f.write("\n\nPlayer O:")
                f.write("\nMaximum depth = " + str(self.d2))
                f.write("\nEuristic = " + str(self.E2))
                f.write("\nMinimax (0) or Alphabeta (1) = " + str(self.a2))

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

    def write_end_game(self, filename):
        with open(filename, 'a') as f:
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
            self.sb_ev_time.append(self.average_ev_time)
            f.write("\nAverage evaluation time of the heuristic for each state evaluated: " + str(self.average_ev_time))

            #6.b.ii
            f.write("\nTotal number of states evaluated during the game: " + str(self.total_nb_states))
            self.sb_total_nb_states.append(self.total_nb_states)

            #6.b.iii
            f.write("\nAverage of per-move average depth")

            #6.b.vi
            f.write("\nTotal number of moves in the game: " + str(self.total_nb_moves))
            self.sb_total_nb_moves.append(self.total_nb_moves)

    def scoreboard_end_game(self):
        with open("scoreboard.txt", 'a') as f:

            for i in range(self.sb_ev_time.__len__()):
                self.sb_av_ev_time += self.sb_ev_time[i]
            for i in range(self.sb_total_nb_states.__len__()):
                self.sb_av_nb_states += self.sb_total_nb_states[i]
            for i in range(self.sb_total_nb_moves.__len__()):
                self.sb_av_nb_moves += self.sb_total_nb_moves[i]

            self.sb_av_ev_time = self.sb_av_ev_time/20
            self.sb_av_nb_states = self.sb_av_nb_states/20
            self.sb_av_nb_moves = self.sb_av_nb_moves/20

            f.write("\nAverage evaluation time of the heuristic for each state evaluated for the whole scoreboard: " + str(self.sb_av_ev_time))

            # 6.b.ii
            f.write("\nTotal number of states evaluated during the game for the whole scoreboard: " + str(self.sb_av_nb_states))

            # 6.b.vi
            f.write("\nTotal number of moves in the game for the whole scoreboard: " + str(self.sb_av_nb_moves))
            f.close()



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

    def check_end(self, e1win, e2win):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is x!')
                e1win += 1
            elif self.result == '0':
                e2win += 1
                print('The winner is 0!')
            elif self.result == '.':
                print("It's a tie!")
            self.write_end_game(self.fileName)

            self.write_end_game("scoreboard.txt")
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
    def e1(self, current_state):  # targets horizontals and vertical
        x = 0
        y = 0
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

        if current_state[x][y] != '.':  # if tiles are full selects 1st empty tile
            for i in range(0, self.n):
                for j in range(0, self.n):
                    if self.current_state[i][j] == '.':
                        x = i
                        y = j

        #self.nb_states_current_move += 1
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

    def minimax(self, depth, d, e, start, t, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        timer = time.time()
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        depth = 0

        if (depth >= d or result) and e == 1 or (round(timer - start, 5) >= t):
            return self.e1(self.current_state)

        if (depth >= d or result) and e == 2 or (round(timer - start, 5) >= t):
            return self.e2(self.current_state)

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    self.total_nb_states += 1
                    if max:  # if max is true
                        self.current_state[i][j] = '0'
                        #for 1 depth
                        (v, _, _) = self.minimax(depth + 1, d, e, start, t, max=False)  # swap turns to min
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        #for 1 depth
                        (v, _, _) = self.minimax(depth + 1, d, e, start, t, max=True)  # swap turns to max
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'

        self.nb_states_current_move += 1
        return 1, x, y

    def alphabeta(self, depth, d, e, start, t, alpha=-2, beta=2, max=False):
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
        timer = time.time()
        result = self.is_end()
        depth = 0

        if (depth >= d or result) and e == 1 or (round(timer - start, 5) >= t):
            return self.e1(self.current_state)

        if (depth >= d or result) and e == 2 or (round(timer - start, 5) >= t):
            return self.e2(self.current_state)


        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    self.total_nb_states += 1
                    if max:
                        self.current_state[i][j] = '0'
                        (v, _, _) = self.alphabeta(depth+1, d, e, start, t, alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(depth+1, d, e, start, t, alpha, beta, max=True)
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

        self.nb_states_current_move += 1
        return (value, x, y)

    def play(self, g_nb, algo=None, player_x=None, player_o=None):
        #global nbs
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN

        while True:
            self.draw_board() #new configuration of the board
            if self.check_end(self.e1win, self.e2win):
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(self.depth, self.d1, self.E1, start, self.t, max=False)
                else:
                    (_, x, y) = self.minimax(self.depth, self.d2, self.E2, start, self.t, max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(self.depth, self.d1, self.E1, start, self.t, max=False)
                else:
                    (m, x, y) = self.alphabeta(self.depth, self.d2, self.E2, start, self.t, max=True)
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

    a = input("Chose Minimax (false) or Alphabeta (true):")
    player_x = input("Chose player x as AI or Human (AI or H)")
    player_o = input("Chose player x as AI or Human (AI or H)")


    r = 10
    if a is False:
        algo = Game.MINIMAX
    else:
        algo = Game.ALPHABETA

    if player_x == "AI":
        player_x = Game.AI
    elif player_x == "H":
        player_x = Game.HUMAN

    if player_o == "AI":
        player_o = Game.AI
    elif player_o == "H":
        player_o = Game.HUMAN

    for i in range(0, 2*r):
        game_nb = i+1
        g.play(game_nb, algo, player_x, player_o)

    Game.writescoreboard(Game)

    with open("scoreboard.txt", 'a') as f:
        f.write("\nNb of games played: " + str(game_nb))
        f.write("\nHeuristic 1 won: " + str(Game.e1win) + " | " + str(Game.e1win / game_nb * 100) + "%")
        f.write("\nHeuristic 2 won: " + str(Game.e2win) + " | " + str(Game.e2win / game_nb * 100) + "%")
        f.close()
    Game.scoreboard_end_game(Game)



if __name__ == "__main__":
    main()