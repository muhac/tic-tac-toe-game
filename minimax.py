import functions
import copy
import random
import numpy as np


def british_museum(board_object, gamer, main):
    winner = board_object.win_state()
    if winner:
        score = {board_object.A: -1,
                 board_object.D: 0,
                 board_object.B: 1}
        return score[winner]

    pos = board_object.draw(False)
    sub = [british_museum(copy.deepcopy(board_object).go(gamer, tg), -1 * gamer, False) for tg in pos]
    rc = max(sub) if gamer == -1 else min(sub)
    if main:
        # return pos[sub.index(rc)]
        index = [i for i in range(len(pos)) if sub[i] == rc]
        random.shuffle(index)
        return pos[index.pop()]
    else:
        return rc


def alpha_beta(board_object, ab, gamer, main):
    winner = board_object.win_state()
    if winner:
        score = {board_object.A: -1,
                 board_object.D: 0,
                 board_object.B: 1}
        return score[winner]

    pos = board_object.draw(False)
    sub = []
    sub_ab = None
    for tg in pos:
        v = alpha_beta(copy.deepcopy(board_object).go(gamer, tg), sub_ab, -1 * gamer, False)
        sub.append(v)
        if ab and ((gamer == -1 and v > ab) or  # MAX player
                   (gamer == 1 and v < ab)):  # MIN player.
            return v  # CUT
        sub_ab = max(sub) if gamer == -1 else min(sub)

    rc = max(sub) if gamer == -1 else min(sub)
    if main:
        index = [i for i in range(len(pos)) if sub[i] == rc]
        random.shuffle(index)
        return pos[index.pop()]
    else:
        return rc


def alpha_beta_symmetry(board_object, ab, gamer, main):
    winner = board_object.win_state()
    if winner:
        score = {board_object.A: -1,
                 board_object.D: 0,
                 board_object.B: 1}
        return score[winner]

    pos = board_object.draw(False)

    b = board_object.board
    if np.array_equal(b, b[:, ::-1]):
        pos = list(set(pos).difference('c', 'f', 'i'))
    if np.array_equal(b, b[::-1, :]):
        pos = list(set(pos).difference('g', 'h', 'i'))
    if np.array_equal(b, b.T):
        pos = list(set(pos).difference('d', 'g', 'h'))
    e_ = np.identity(b.shape[0])[:, ::-1]
    if np.array_equal(b, e_.dot(b.T).dot(e_)):
        pos = list(set(pos).difference('f', 'h', 'i'))

    sub = []
    sub_ab = None
    for tg in pos:
        v = alpha_beta_symmetry(copy.deepcopy(board_object).go(gamer, tg), sub_ab, -1 * gamer, False)
        sub.append(v)
        if ab and ((gamer == -1 and v > ab) or  # MAX player
                   (gamer == 1 and v < ab)):  # MIN player.
            return v  # CUT
        sub_ab = max(sub) if gamer == -1 else min(sub)

    rc = max(sub) if gamer == -1 else min(sub)
    if main:
        index = [i for i in range(len(pos)) if sub[i] == rc]
        random.shuffle(index)
        return pos[index.pop()]
    else:
        return rc
