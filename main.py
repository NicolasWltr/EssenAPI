from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from flask_socketio import SocketIO
from datetime import timedelta
from datetime import datetime
import os
import json
import requests as rq
import chatbot as cb

app = Flask(__name__)
app.secret_key = 'asdfghjklöä'
app.static_folder = 'static'

socketio = SocketIO(app, cors_allowed_origins='ws://walternicolas.de:80')

import gameCalls

current_dir = os.path.dirname(os.path.abspath(__file__))
login_file_path = os.path.join(current_dir, 'data', 'login.json')
saver_file_path = os.path.join(current_dir, 'data', 'save.json')

with open(login_file_path) as file:
    logins = json.load(file)

lastCalled = datetime.now() - timedelta(hours=3)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login():
    if checkForSession() == 'login':
        return render_template('login.html')

    if session.__contains__('loginerror'):
        return redirect(url_for('start', error=session['loginerror'], username=session['username']))

    return redirect(url_for('start'))



@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    usernameFromForm = request.form['username']
    passwordFromForm = request.form['password']

    for login in logins:
        if login['username'] == usernameFromForm:
            if login['password'] == passwordFromForm:
                session['currentUser'] = login['username']
                session['hash'] = hash(login['username']) + hash(login['password'])
                cb.send(session['currentUser'] + ' has logged in')
                return redirect(url_for('start'))
            else:
                session['usernameFromForm'] = usernameFromForm
                session['loginerror'] = 'Invalid username or password'
                return redirect(url_for('login'))

    session['usernameFromForm'] = usernameFromForm
    session['loginerror'] = 'Invalid username or password'
    return redirect(url_for('login'))


@app.route('/logout', methods=['GET'])
def logout():
    if session.__contains__('hash'):
        session.pop('hash')
        cb.send(session['currentUser'] + ' has logged out')
    return redirect(url_for('login'))


@app.route('/start', methods=['GET'])
def start():
    if checkForSession() == "login":
        return redirect(url_for('login'))
    return render_template("start.html")


@app.route('/load', methods=['GET'])
def load():
    if checkForSession() == "login":
        return redirect(url_for('login'))
    return render_template("load.html")


@app.route('/checkID', methods=['POST'])
def checkID():
    if checkForSession() == "login":
        return redirect(url_for('login'))

    with open(saver_file_path) as file:
        saves = json.load(file)

    idFromForm = request.form.get('id')

    for save in saves:
        if save['id'] == idFromForm:
            session['id'] = idFromForm
            return render_template("saved.html")

    return redirect(url_for('IDNotPresent'))


@app.route('/checkIDCreated', methods=['POST'])
def checkIDCreated():
    if checkForSession() == "login":
        return redirect(url_for('login'))

    id = request.form.get('id')

    with open(saver_file_path) as file:
        saves = json.load(file)
        for save in saves:
            if save['id'] == id:
                return render_template("alreadyExists.html")

        additional = {
            "id": id,
            "input": ''
        }

        saves.append(additional)

    with open(saver_file_path, 'w') as file:
        json.dump(saves, file)

    session['id'] = id
    return render_template("saved.html")


@app.route('/createID', methods=['GET'])
def createID():
    if checkForSession() == "login":
        return redirect(url_for('login'))

    return render_template("createSave.html")


@app.route('/IDNotPresent', methods=['GET'])
def IDNotPresent():
    if checkForSession() == "login":
        return redirect(url_for('login'))

    return render_template("wrongID.html")


@app.route('/deleteID', methods=['GET'])
def deleteID():
    if checkForSession() == "login":
        return redirect(url_for('login'))

    return render_template("deleteID.html")


@app.route('/checkForIDdelete', methods=['POST'])
def checkForIDdelete():
    if checkForSession() == "login":
        return redirect(url_for('login'))

    idToDelete = request.form.get('id')

    with open(saver_file_path) as file:
        saves = json.load(file)

        idOf = 0

        for save in saves:
            if save['id'] == idToDelete:
                del saves[idOf]
                break
            idOf = idOf + 1

    with open(saver_file_path, 'w') as file:
        json.dump(saves, file)

    return redirect(url_for('start'))


@app.route('/api/getAllAvailableAPICalls', methods=['GET'])
def getAllAvailableAPICalls():
    return jsonify([
        {
            "name": "essen", "url": "http://walternicolas.de/apiWP/essen", "type": "call"
        },
        {
            "name": "resetTimer", "url": "http://walternicolas.de/apiWP/resetTimer", "type": "call"
        },
        {
            "name": "Pause/Play", "url": "http://walternicolas.de/apiWP/pp", "type": "call"
        },
        {
            "name": "stop", "url": "http://walternicolas.de/apiWP/stop", "type": "call"
        },
        {
            "name": "Shutdown", "url": "http://walternicolas.de/apiWP/shutdown", "type": "call"
        },
        {
            "name": "Stop Shutdown", "url": "http://walternicolas.de/apiWP/shutdownstop", "type": "call"
        }
    ])


@app.route('/getter/getAllSaves', methods=['GET'])
def getAllSaves():
    if request.headers.get('Token') != 'nivanprpquß24723h780cnß2n1n':
        return "declined"

    with open(saver_file_path) as file:
        saves = json.load(file)

    saveIDs = []

    for save in saves:
        saveIDs.append(save['id'])

    return jsonify(saveIDs)


@app.route('/getter/getsave', methods=['GET'])
def getSave():
    if request.headers.get('Token') != 'nivanprpquß24723h780cnß2n1n':
        return "declined"

    with open(saver_file_path) as file:
        saves = json.load(file)

    for save in saves:
        if save['id'] == session['id']:
            return save['input']


@app.route('/setter/setsave', methods=['POST'])
def setsave():
    if request.headers.get('Token') != 'nivanprpquß24723h780cnß2n1n':
        return "declined"

    inputForId = request.args.get("input")

    with open(saver_file_path) as file:
        saves = json.load(file)

    for save in saves:
        if save['id'] == session['id']:
            save['input'] = inputForId

    with open(saver_file_path, 'w') as file:
        json.dump(saves, file)

    return "saved"


def checkForSession():
    if session.__contains__('hash'):
        return "Yes"
    else:
        return "login"


def checkForHeader():
    if request.headers.get('Token') == '1074473':
        return "Yes"
    else:
        return "denied"


# Call functions on PC
@app.route('/apiWP/essen', methods=['GET'])
def essen():
    if checkForHeader() == "denied":
        if not (request.args.get('token') == "MyMumCanUseThisEveryTime"):
            return "denied"
        else:
            session['currentUser'] = 'Mama'

    url = "http://192.168.178.72:25565/essen"

    headers = {'Token': '1074473'}

    cb.send(session['currentUser'] + ' hat zum Essen gerufen')

    response = rq.get(url, headers=headers)

    cb.send('Antwort => ' + response.text)

    return response.text


@app.route('/apiWP/resetTimer', methods=['GET'])
def resetTimer():
    if checkForHeader() == "denied":
        return "denied"

    url = "http://192.168.178.72:25565/resetTimer"

    headers = {'Token': '1074473'}

    cb.send(session['currentUser'] + ' hat den Timer resettet')

    response = rq.get(url, headers=headers)

    cb.send('Antwort => ' + response.text)

    return response.text


@app.route('/apiWP/pp', methods=['GET'])
def pp():
    if checkForHeader() == "denied":
        return "denied"

    url = "http://192.168.178.72:25565/pp"

    headers = {'Token': '1074473'}

    cb.send(session['currentUser'] + ' hat Play/Pause gedrückt')

    response = rq.get(url, headers=headers)

    cb.send('Antwort => ' + response.text)

    return response.text


@app.route('/apiWP/stop', methods=['GET'])
def stop():
    if checkForHeader() == "denied":
        return "denied"

    url = "http://192.168.178.72:25565/stop"

    headers = {'Token': '1074473'}

    cb.send(session['currentUser'] + ' hat den Endpunkt am PC gestoppt')

    response = rq.get(url, headers=headers)

    cb.send('Antwort => ' + response.text)

    return response.text


@app.route('/apiWP/shutdown', methods=['GET'])
def shutdown():
    if checkForHeader() == "denied":
        return "denied"

    url = "http://192.168.178.72:25565/shutdown"

    headers = {'Token': '1074473'}

    cb.send(session['currentUser'] + ' hat den Computer heruntergefahren')

    response = rq.get(url, headers=headers)

    cb.send('Antwort => ' + response.text)

    return response.text


@app.route('/apiWP/shutdownstop', methods=['GET'])
def shutdownstop():
    if checkForHeader() == "denied":
        return "denied"

    url = "http://192.168.178.72:25565/shutdownstop"

    headers = {'Token': '1074473'}

    cb.send(session['currentUser'] + ' hat das herunterfahren abgebrochen')

    response = rq.get(url, headers=headers)

    cb.send('Antwort => ' + response.text)

    return response.text


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    # app.run(host='0.0.0.0', threaded=True)



