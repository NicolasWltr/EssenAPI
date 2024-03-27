from flask import Flask, request, jsonify, redirect, url_for, render_template, session, make_response
import subprocess
from datetime import timedelta
from datetime import datetime
import os, signal
import winsound
#import win32api
#import win32con
import json

app = Flask(__name__)
app.secret_key = 'asdfghjklöä'
app.static_folder = 'static'


current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file_path = os.path.join(current_dir, 'data', 'login.json')

with open(credentials_file_path) as file:
    logins = json.load(file)

lastCalled = datetime.now() - timedelta(hours=3)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    usernameFromForm = request.form['username']
    passwordFromForm = request.form['password']

    for login in logins: 
        if login['username'] == usernameFromForm:
            if login['password'] == passwordFromForm:
                session['currentUser'] = login['username']
                session['hash'] = hash(login['username']) + hash(login['password'])
                return render_template('check.html')
            else:
                return "Wrong Username and Password Pair"

    return "Wrong Username and Password Pair"


@app.route('/essen', methods=['GET'])
def essen():
    if checkForHeader() == "denied":
        if not(request.args.get('token') == "MyMumCanUseThisEveryTime"):
            return "access denied"

    global lastCalled
    if lastCalled > datetime.now() - timedelta(minutes=30):
        nextCalled = lastCalled + timedelta(minutes=30)
        return "Nicolas kann erst wieder gerufen werden am " + nextCalled.date().__str__() + " um " + nextCalled.time().__str__()
    lastCalled = datetime.now()
    subprocess.run([r"script.bat"])
    winsound.Beep(1000, 1000)
    response = "Nicolas wurde zum essen gerufen am " + lastCalled.date().__str__() + " um " + lastCalled.time().__str__()
    return response


@app.route('/resetTimer', methods=['GET'])
def resetTimer():
    if checkForHeader() == "denied":
        return "access denied"
    
    global lastCalled
    lastCalled = datetime.now() - timedelta(hours=3)
    return "Timer reseted successfully!"


@app.route('/pp', methods=['GET'])
def playpause():
    if checkForHeader() == "denied":
        return "access denied"
    
    VK_MEDIA_PLAY_PAUSE = 0xB3
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0, 0)
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, win32con.KEYEVENTF_KEYUP, 0)
    return "Success"


@app.route('/stop', methods=['GET'])
def stop():
    if checkForHeader() == "denied":
        return "access denied"
    
    os.kill(os.getpid(), signal.SIGINT)
    return "Stopped"


@app.route('/shutdown', methods=['GET'])
def shoutdown():
    if checkForHeader() == "denied":
        return "access denied"
    
    os.system('shutdown -s')
    return "Shutdown!"


@app.route('/shutdownstop', methods=['GET'])
def shoutdownstop():
    if checkForHeader() == "denied":
        return "access denied"
    
    os.system('shutdown -a')
    return "Shutdown abgebrochen!"


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25565, threaded=True)
    
