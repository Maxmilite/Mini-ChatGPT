import uuid
from flask import make_response, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import asyncio
import nest_asyncio
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS, cross_origin
import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
from gevent import monkey
monkey.patch_all()

# Flask
client = 'http://127.0.0.1:5173'
currentConnection = 0
app = Flask(__name__)

# CORS(app, supports_credentials=True, origins=client)
# @app.after_request
# def getResponse(response):
#     # response = make_response()
#     whiteList = [client]
#     response.headers["Access-Control-Allow-Origin"] = client
#     response.headers["Access-Control-Allow-Credentials"] = 'true'
#     return response

# Async IO
nest_asyncio.apply()
maxConnection = 3
loop = asyncio.get_event_loop()

# Thread Pool
executor = ThreadPoolExecutor()

# Login and Session
app.secret_key = b'a*DMp_V%q_sQ27~5'
loginManager = LoginManager()
loginManager.init_app(app)
users = [
    {
        "id": uuid.uuid4(),
        "username": "1",
        "password": generate_password_hash("1")
    }
]


def createUser(user_name, password):
    user = {
        "username": user_name,
        "password": generate_password_hash(password),
        "id": uuid.uuid4()
    }
    users.append(user)


def getUser(user_name):
    for user in users:
        if user.get("username") == user_name:
            return user
    return None


class User(UserMixin):
    """User Class"""

    def __init__(self, user):
        self.username = user.get("username")
        self.password_hash = user.get("password")
        self.id = user.get("id")

    def verifyPassword(self, password):
        """Password Verification"""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def getID(self):
        """Get User ID"""
        return self.id

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        for user in users:
            if user.get('id') == user_id:
                return User(user)
        return None


@loginManager.user_loader
def load_user(user_id):
    return User.get(user_id)


# MySQL Connection
'''
A SQL Server with a database called $nameDatabaseMessage is needed. 
'''

address = "localhost"
port = 3306
nameMessageDatabase = "MessageTemplate"
nameMessageTable = "message_table"
username = "guest"
password = "dnf@#YU328!4#NYVJ"
unknownMessage = "Unknown message."

db = MySQLdb.connect(address, username, password,
                     nameMessageDatabase, charset='utf8')
cursor = db.cursor()

# Internal Function


def updatePopularity(message):
    cursor.execute(
        "SELECT id,popularity FROM message_table WHERE question=\"" + message + "\"")
    data = cursor.fetchone()
    val = int(data[1]) + 1
    id = int(data[0])
    cursor.execute("UPDATE `messagetemplate`.`message_table` SET `popularity` = \'" +
                   str(val) + "\' WHERE (`id` = \'" + str(id) + "\')")
    db.commit()

# API


@app.route('/')
def main():
    return "Invalid arguments"


@app.route('/api/message', methods=['GET'])
def getMessage():
    message = request.args.get('message', '').replace(
        "?", "").replace(".", "").replace("？", "")
    global currentConnection
    if currentConnection >= maxConnection:
        return "Access Denied."
    currentConnection += 1
    cursor.execute(
        "SELECT answer FROM message_table WHERE question=\"" + message + "\"")
    data = cursor.fetchone()
    currentConnection -= 1
    if (data != None):
        updatePopularity(message)
        return data[0]
    else:
        return unknownMessage


@app.route('/api/autocomplete', methods=['GET'])
def getACList():
    cursor.execute(
        "SELECT question FROM message_table")
    data = cursor.fetchall()
    return jsonify([{"value": i[0]} for i in data])


@app.route('/api/hotspot', methods=['GET'])
def getHotSpot():
    cursor.execute(
        "SELECT question,answer,popularity FROM message_table ORDER BY popularity DESC")
    data = cursor.fetchall()
    return jsonify([{"question": i[0], "answer": i[1], "popularity": i[2], "rank": data.index(i) + 1} for i in data])

@app.route('/api/login', methods=['POST'])
def login():
    session.clear()
    try:
        loginJson = request.get_json()
    except Exception:
        loginJson = {}
    if not loginJson:
        loginJson = {}
    username = loginJson.get("username")
    password = loginJson.get("password")
    if not all([username, password]):
        return jsonify(code=400, msg="Invalid argument")
    userInfo = getUser(username)
    if userInfo is None:
        createUser(username, password)
        userInfo = getUser(username)
    user = User(userInfo)
    if user.verifyPassword(password):
        login_user(user, remember=True)
        return jsonify(code=200, msg="Login success")
    else:
        return jsonify(code=401, msg="Incorrect username or password")


@app.route("/api/session", methods=["GET"])
def check_session():
    username = session.get("username")
    if username:
        return jsonify(code=200, msg=username)
    else:
        return jsonify(code=401, msg="Not logged in")


@app.route("/api/logout")
# @cross_origin(supports_credentials=True, origins=client)
@login_required
def logout():
    logout_user()
    return jsonify(code=200, msg="Success")


# Main

if __name__ == "__main__":
    from werkzeug.debug import DebuggedApplication
    from gevent import pywsgi
    dapp = DebuggedApplication(app, evalex=True)
    app.jinja_env.auto_reload = True
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()