import minimax
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'tictactoegame'


def draw_board(brd):
    b = ''
    for i in range(9):
        if brd[i] == 0:
            b += f'<label><input type="radio" name="box" value="{i}"><div>©</div></label>'
        elif brd[i] == -1:
            b += '<label><input type="radio" name="box" disabled><div class="tree">○</div></label>'
        else:
            b += '<label><input type="radio" name="box" disabled><div class="human">X</div></label>'
    return b


@app.route('/demo/tic-tac-toe/', methods=('GET', 'POST'))
def index():
    winner = ''
    board = np.zeros(9)

    # start game
    if request.form.get('p'):
        if request.form.get('p') == 'T':
            board = np.array([-1, 0, 0, 0, 0, 0, 0, 0, 0])
            np.random.shuffle(board)
        else:
            board = np.zeros(9)

    # next step
    if request.form.get('brd'):
        board = np.array([int(i) for i in request.form.get('brd').split('|')])

        if request.form.get('box'):
            board[int(request.form.get('box'))] = 1
            winner = minimax.win_state(board.reshape(3, 3))
            if not winner:
                choice = minimax.alpha_beta(board.reshape(3, 3), None, -1, True)
                board[choice] = -1
                winner = minimax.win_state(board.reshape(3, 3))

    brd = '|'.join([str(int(i)) for i in board.tolist()])
    display = draw_board(board)

    return render_template('main.html',
                           game=f'<label style="display:none;"><input name="brd" value={brd}></label>',
                           display=display, win=winner)


app.run(port=30001)
