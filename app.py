from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "some-secret"

debug = DebugToolbarExtension(app)

from boggle import Boggle

boggle_game = Boggle()


###   ROUTING   ###
#Homepage
@app.route('/')
def homepage():
    """Show homepage"""

    board = boggle_game.make_board()

    session['board'] = board
    highscore = session.get("highscore", 0)
    tries = session.get("tries", 0)

    return render_template('base.html', board=board, highscore=highscore, tries=tries)

#guess word
@app.route('/check-guess')
def guess_word():
    """Takes user guess and checks its validity"""

    word = request.args['word']

    validity = boggle_game.check_valid_word(session['board'], word)

    return jsonify({"result": validity})

#score logging
@app.route('/store-score', methods=['POST'])
def store_score():
    """On game finish, score high score and number of plays"""
    
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    tries = session.get("tries", 0)

    session['tries'] = tries + 1
    session['highscore'] = max(score, highscore)

    is_new_highscore = True if (score > highscore) else False

    return jsonify(is_new_highscore)