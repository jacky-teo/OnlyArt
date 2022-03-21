## Microservice to store who is subscribed to who ##
from audioop import add
from http.client import CREATED
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/onlyfence'
# root@localhost will change
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class creatorAccount(db.Model):
    __tablename__ = "creatoraccount"

    CREATORID = db.Column(db.String(64), primary_key=True, nullable=False)
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


class subscriptionLink(db.Model):
    __tablename__ = 'subscription_link'

    CREATORID = db.Column(db.String(64), primary_key=True, nullable=False)
    CONSUMERID = db.Column(db.String(64), primary_key=True, nullable=False)
    CREATED = db.Column(db.ForeignKey(
        'creatoraccount.CREATORID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    MODIFIED = db.Column(db.ForeignKey(
        'consumeraccount.CONSUMERID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    def __init__(self, CREATORID, CONSUMERID, CREATED, MODIFIED):
        self.CREATORID = CREATORID
        self.CONSUMERID = CONSUMERID
        self.CREATED = CREATED
        self.MODIFIED = MODIFIED

    def json(self):
        return {"CREATORID": self.CREATORID, "CONSUMERID": self.CONSUMERID, "CREATED": self.CREATED, "MODIFIED": self.MODIFIED}

# scenario 1 & 4
@app.route('/subscription/status')
def get_all():
    data = request.get_json()
    creatorid = data["CREATORID"]
    consumerid = data["CONSUMERID"]
    status = subscriptionLink.query.filter_by(
        CREATORID=creatorid, CONSUMERID=consumerid).first()

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
            "message": "Not subscribed."
            # will change to page rendering/rerouting
        }
    ), 404

# scenario 2
@app.route('/subscription/add', methods=["POST"])
def create_subscription():
    creatorid = request.json.get('CREATORID')
    consumerids = request.json.get('CONSUMERIDS')

    for consumerid in consumerids:
        if (subscriptionLink.query.filter_by(CREATORID=creatorid, CONSUMERID=consumerid).first()):
            return jsonify(
                {
                    "code": 400,
                    "message": "Already subscribed."
                }
            ), 400
        else: 
            created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            modified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            subcribedParing = subscriptionLink(CREATORID=creatorid, CONSUMERID=consumerid, CREATED=created, MODIFIED=modified)

            try:
                db.session.add(subcribedParing)
                db.session.commit()
            except Exception as e:
                return jsonify(
                    {
                        "code": 500,
                        "message": "An error occurred creating subscription link" + str(e)
                    }
                ), 500
            return jsonify(
                {
                    "code": 201,
                    "message": "Subscription link created"
                }
            ), 201

# scenario 3
@app.route('/subscription/getsubscribers/<string:creatorid>')
def get_all_subscribers(creatorid):
    creator_consumer = subscriptionLink.query.filter_by(CREATORID=creatorid)

    if creator_consumer:
        for crco in creator_consumer:
            return jsonify({
                "code":200,
                "data":[crco.CONSUMERID for crco in creator_consumer]
            }), 200
    return jsonify({
        "code":404,
        "message":"Creator does not exist"
        }
    ),404         


if __name__ == '__main__':
    app.run(port=5001, debug=True)
