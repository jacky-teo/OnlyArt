## Microservice to store creator account information ##
from audioop import add
from http.client import CREATED
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:3306/creator'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class creatorAccount(db.Model):
    __tablename__ = "creatoraccount"

    CREATORID = db.Column(db.String(64), primary_key=True)
    USERNAME = db.Column(db.String(64), nullable=False)
    PASSWORD = db.Column(db.String(64), nullable=False)
    EMAIL = db.Column(db.String(64), nullable=False)
    PRICE = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, CREATORID, USERNAME, PASSWORD, EMAIL, PRICE):
        self.CREATORID = CREATORID
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.EMAIL = EMAIL
        self.PRICE = PRICE

    def json(self):
        return {"CREATORID": self.CREATORID, "USERNAME": self.USERNAME, "PASSWORD": self.PASSWORD, "EMAIL": self.EMAIL, "PRICE": self.PRICE}

# scenario 1
@app.route('/creator/price')
def get_creator_price():
    data = request.get_json()
    creatorid = data["CREATORID"]
    status = creatorAccount.query.filter_by(
        CREATORID=creatorid).first()

    if (status):
        return jsonify(
            {
                "code": 200,
                "data": status.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Creator does not exist."
        }
    ), 404

@app.route('/creator')
def get_all():
    creatorlist = creatorAccount.query.all()
    if len(creatorlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "creators": [creator.json() for creator in creatorlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no creators."
        }
    ), 404

# scenario 4
@app.route('/creator/getinfo/<string:creatorid>')
def get_info(creatorid):
    status = creatorAccount.query.filter_by(
        CREATORID=creatorid).first()

    if (status):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "username":status.USERNAME,
                    "email": status.EMAIL}
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Creator does not exist."
        }
    ), 404


if __name__ == '__main__':
    app.run(port=5002, debug=True)
