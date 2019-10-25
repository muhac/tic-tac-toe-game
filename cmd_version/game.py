import functions
import minimax
import os

if __name__ == '__main__':
    b = functions.Board()
    gamer = -1 if input('Human first? [Y/n] ').upper() == 'N' else 1
    print('Human: X, Tree: O\n')

    while True:
        if gamer == 1:
            b.draw()
            go = b.map[input('  -> ')]
        else:
            go = minimax.alpha_beta(b, None, gamer, True)
            print(f'     {b.map_inv[go]} <-')

        b.go(gamer, go)
        state = b.win_state()
        if state:
            b.draw()
            print(state)
            break
        else:
            gamer *= -1

    os.system('pause')
