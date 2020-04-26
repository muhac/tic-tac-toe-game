import numpy as np
from random import randint


class Board(object):
    def __init__(self):
        self.A = 'Human wins.'
        self.B = 'Tree wins.'
        self.D = 'No one wins.'

        self.board = np.zeros([3, 3])

        # Using symmetry to get rid of duplicates
        # but this will make the ai always work around a certain corner
        # randomly rotate the board to make every games looks different
        self.rot = randint(1, 4)
        true_board = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])
        show_board = np.rot90(true_board.reshape((3, 3)), self.rot).flatten()
        self.map = dict(zip(show_board, true_board))
        self.map_inv = dict(zip(true_board, show_board))

    def win_state(self):
        """
        Check if any player wins or game ends.
        :return: game state
        """
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
        """
        Place a piece.
        :return: board object of the game
        """
        p2m = {'a': (0, 0), 'b': (0, 1), 'c': (0, 2),
               'd': (1, 0), 'e': (1, 1), 'f': (1, 2),
               'g': (2, 0), 'h': (2, 1), 'i': (2, 2)}
        self.board[p2m[position]] = gamer
        return self

    def draw(self, output=True):
        """
        Print the board out. Also used to get positions available in minimax program.
        :param output: print it out or not
        :return: list of all available positions
        """
        true_board = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])
        filled_board = self.board.flatten()
        available = [true_board[i] for i in range(9) if filled_board[i] == 0]

        if output:  # show transformed board
            show_board = np.rot90(true_board.reshape((3, 3)), self.rot).flatten()
            for i in range(9):
                if filled_board[i] == 1:
                    show_board[i] = 'X'
                elif filled_board[i] == -1:
                    show_board[i] = 'O'
            show_board = np.rot90(show_board.reshape((3, 3)), -self.rot)
            for x in show_board:
                print(' '.join(x.tolist()))

        return available
