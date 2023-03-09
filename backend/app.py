from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import MySQLdb

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

db = MySQLdb.connect(address, username, password, nameMessageDatabase, charset='utf8')
cursor = db.cursor()

# Flask
app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/')
def main():
    return "Invalid arguments"

@app.route('/message', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def getMessage():
    message = request.args.get('message', '').replace("?", "").replace(".", "")
    cursor.execute("SELECT answer FROM message_table WHERE question=\"" + message + "\"")
    data = cursor.fetchone()
    print(data)
    if (data == None):
        return unknownMessage
    else:
        return data[0]



if __name__ == "app":
    None