from main import app


@app.route('/testGame')
def test_game():
    return "Hello World!"
