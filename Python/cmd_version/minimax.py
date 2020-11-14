import functions
import copy
import random
import numpy as np


def alpha_beta(board_object, ab, gamer, main):
    """
    Search for the best choice.
    :param board_object: current board
    :param ab: alpha / beta value
    :param gamer: max-player (ai, -1) or the min-player (human, 1)
    :param main: whether it is called by the main function (need a choice instead of a value)
    :return: the best position found
    """
    winner = board_object.win_state()
    if winner:
        score = {board_object.A: -1,
                 board_object.D: 0,
                 board_object.B: 1}
        return score[winner]

    next_step = board_object.draw(False)

    # find symmetry
    b = board_object.board
    # horizontal
    if np.array_equal(b, b[:, ::-1]):
        next_step = list(set(next_step).difference('c', 'f', 'i'))
    # vertical
    if np.array_equal(b, b[::-1, :]):
        next_step = list(set(next_step).difference('g', 'h', 'i'))
    # diagonal
    if np.array_equal(b, b.T):
        next_step = list(set(next_step).difference('d', 'g', 'h'))
    if np.array_equal(np.rot90(b), np.rot90(b).T):
        next_step = list(set(next_step).difference('f', 'h', 'i'))

    sub = []
    sub_ab = None
    for tg in next_step:
        v = alpha_beta(copy.deepcopy(board_object).go(gamer, tg), sub_ab, -gamer, False)
        sub.append(v)
        if ab and ((gamer == -1 and v > ab) or  # MAX player
                   (gamer == 1 and v < ab)):    # MIN player.
            return v                            # CUT
        sub_ab = max(sub) if gamer == -1 else min(sub)

    if main:
        candidates = [next_step[i] for i in range(len(next_step)) if sub[i] == sub_ab]
        random.shuffle(candidates)
        return candidates.pop()
    else:
        return sub_ab
