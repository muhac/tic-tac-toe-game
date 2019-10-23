import numpy as np
from random import randint


class Board(object):
    def __init__(self):
        self.A = 'Human'
        self.B = 'Tree'
        self.D = 'No one'

        self.board = np.zeros([3, 3])

        self.rot = randint(1, 4)         # to make games different visually
        true_board = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])
        show_board = np.rot90(true_board.reshape((3, 3)), self.rot).flatten()
        self.map = dict(zip(show_board, true_board))

    def win_state(self):
        unfilled = np.sum(self.board == 0)
        if not unfilled:
            win = self.D
        else:
            win = False

        win_check = [self.board[0, 0] if abs(sum(self.board[0, :])) == 3 else False,
                     self.board[1, 0] if abs(sum(self.board[1, :])) == 3 else False,
                     self.board[2, 0] if abs(sum(self.board[2, :])) == 3 else False,

                     self.board[0, 0] if abs(sum(self.board[:, 0])) == 3 else False,
                     self.board[0, 1] if abs(sum(self.board[:, 1])) == 3 else False,
                     self.board[0, 2] if abs(sum(self.board[:, 2])) == 3 else False,

                     self.board[1, 1] if abs(sum(np.diag(self.board))) == 3 else False,
                     self.board[1, 1] if abs(sum(np.diag(np.fliplr(self.board)))) == 3 else False]

        for check in win_check:
            if check:
                win = self.A if check == 1 else self.B
                break

        return win

    def go(self, gamer, position):
        pos2arr = {'a': (0, 0), 'b': (0, 1), 'c': (0, 2),
                   'd': (1, 0), 'e': (1, 1), 'f': (1, 2),
                   'g': (2, 0), 'h': (2, 1), 'i': (2, 2)}
        self.board[pos2arr[position]] = gamer
        return self

    def draw(self, output=True):
        true_board = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])
        filled = self.board.flatten()
        available = [true_board[i] for i in range(9) if filled[i] == 0]

        if output:          # only the board shown to player is transformed
            show_board = np.rot90(true_board.reshape((3, 3)), self.rot).flatten()
            for i in range(9):
                if filled[i] == 1:
                    show_board[i] = 'X'
                elif filled[i] == -1:
                    show_board[i] = 'O'
            show_board = np.rot90(show_board.reshape((3, 3)), -self.rot)
            for x in show_board:
                print(' '.join(x.tolist()))

        return available
