from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bOggleTime'  # Set a secret key for session management

boggle_game = Boggle()

@app.route("/")
def home():
    board = boggle_game.make_board()  # Generate a new Boggle board
    session['board'] = board  # Store the board in the session
    return render_template("board.html", board=board)

@app.route("/how_to_play")
def how_to_play():
    return render_template("how_to_play.html")

@app.route("/guess", methods=["POST"])
def handle_guess():
    try:
        guess = request.json.get("guess", "").upper()
        print(f"Guess received: {guess}")  # Debug: Print the received guess
        board = session.get('board', [])
        result = boggle_game.check_valid_word(board, guess)
        print(f"Check result: {result}")  # Debug: Print the check result
        return jsonify({"result": result})
    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred'}), 500
    
@app.route("/new-game")
def new_game():
    # Logic to set up a new game, e.g., resetting the board in session
    return redirect(url_for('/'))  # Assuming 'home' is the route where your game starts

@app.route("/game-statistics", methods=["POST"])
def update_game_statistics():
    """
    Update game statistics including the number of plays and the highest score.
    Receives the current score from the frontend and compares it with the highest score stored in session.
    Increments the number of plays.
    """
    if not request.json or 'score' not in request.json:
        return jsonify({'error': 'Missing score'}), 400

    current_score = request.json['score']
    highest_score = session.get('highest_score', 0)
    num_plays = session.get('num_plays', 0) + 1  # Increment the number of plays

    # Update highest score if current score is greater
    if current_score > highest_score:
        session['highest_score'] = current_score

    # Update the session with the new number of plays
    session['num_plays'] = num_plays

    # Return the updated statistics to the client
    return jsonify({
        'highest_score': session.get('highest_score'),
        'num_plays': session.get('num_plays')
    })