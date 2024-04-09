from main import app


@app.route('koopgames/hostGame', methods=['GET'])
def hostGame():
    return "Game Pin"


@app.route('/koopgames/joinGame', methods=['POST'])
def join_game():
    return "Join Game Pin"
