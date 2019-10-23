import copy
import random
import numpy as np


def win_state(board):
    unfilled = np.sum(board == 0)
    if not unfilled:
        win = "No one wins."
    else:
        win = False

    win_check = [board[0, 0] if abs(sum(board[0, :])) == 3 else False,
                 board[1, 0] if abs(sum(board[1, :])) == 3 else False,
                 board[2, 0] if abs(sum(board[2, :])) == 3 else False,

                 board[0, 0] if abs(sum(board[:, 0])) == 3 else False,
                 board[0, 1] if abs(sum(board[:, 1])) == 3 else False,
                 board[0, 2] if abs(sum(board[:, 2])) == 3 else False,

                 board[1, 1] if abs(sum(np.diag(board))) == 3 else False,
                 board[1, 1] if abs(sum(np.diag(np.fliplr(board)))) == 3 else False]

    for check in win_check:
        if check:
            win = "Human wins." if check == 1 else "Tree wins."
            break

    return win


def go(board, gamer, position):
    pos2arr = {'1': (0, 0), '2': (0, 1), '3': (0, 2),
               '4': (1, 0), '5': (1, 1), '6': (1, 2),
               '7': (2, 0), '8': (2, 1), '9': (2, 2)}
    board[pos2arr[position]] = gamer
    return board


def possible(board):
    blank = np.array(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    filled = board.flatten()
    available = [blank[i] for i in range(9) if filled[i] == 0]
    return available


def alpha_beta(board, ab, gamer, main):
    winner = win_state(board)
    if winner:
        score = {"Human wins.": -1,
                 "No one wins.": 0,
                 "Tree wins.": 1}
        return score[winner]

    pos = possible(board)

    sub = []
    sub_ab = None
    for tg in pos:
        v = alpha_beta(go(copy.deepcopy(board), gamer, tg), sub_ab, -gamer, False)
        sub.append(v)
        if ab and ((gamer == -1 and v > ab) or  # MAX player
                   (gamer == 1 and v < ab)):    # MIN player.
            return v                            # CUT
        sub_ab = max(sub) if gamer == -1 else min(sub)

    rc = max(sub) if gamer == -1 else min(sub)
    if main:
        index = [i for i in range(len(pos)) if sub[i] == rc]
        random.shuffle(index)
        return pos[index.pop()]
    else:
        return rc
