## Microservice to store consumer information ##
from audioop import add
from http.client import CREATED
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:3306/consumer'
# root@localhost will change
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class consumerAccount(db.Model):
    __tablename__ = "consumeraccount"

    CONSUMERID = db.Column(db.String(64), primary_key=True, nullable=False)
    USERNAME = db.Column(db.String(64), nullable=False)
    PASSWORD = db.Column(db.String(64), nullable=False)
    TELEGRAM = db.Column(db.String(64), nullable=False)

    def __init__(self, CONSUMERID, USERNAME, PASSWORD, TELEGRAM):
        self.CONSUMERID = CONSUMERID
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.TELEGRAM = TELEGRAM

    def json(self):
        return {"CONSUMERID": self.CONSUMERID, "USERNAME": self.USERNAME, "PASSWORD": self.PASSWORD, "TELEGRAM": self.TELEGRAM}

@app.route("/consumer/retrievetelegram")
def get_telegram():
    data = request.get_json() 
    consumerlist = []
    consumers = data["data"]

    for consumer in consumers:
        response = consumerAccount.query.filter_by(CONSUMERID=consumer).first()
        if response:
            consumerlist.append(response.TELEGRAM)
    if len(consumerlist)== 0:
        return jsonify({
            "code": 404,
            "message": "No consumer telegram tags were found."
        }), 404
    else:
        return jsonify({
                "code": 200,
                "data": consumerlist
            }), 200

#creator account authentication
@app.route("/consumer/authenticate", methods=['POST'])
def creator_auth():
    print('-----authenticating creator-----')
    data = request.args
    username = data.get('username')
    status = consumerAccount.query.filter_by(USERNAME=username).first()

    if (status):
        password = data.get('password')
        isVerified = True if status.PASSWORD == password else False     #verifies if password matches user's password

        if (isVerified):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "consumerID": status.CONSUMERID 
                    },
                    "message": "Consumer exists!"
                }
            )
        
        return jsonify(
            {
                "code": 204,
                "message": "Incorrect credentials"
            }
        )

    #username not found
    return jsonify(
        {
            "code": 404,
            "message": "Consumer does not exist"
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)
