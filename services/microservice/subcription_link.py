## Microservice to store who is subscribed to who ##
from audioop import add
from http.client import CREATED
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:3306/onlyfence'
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

# scenario 1


@app.route('/subscriptionstatus')
def get_subscription_status():
    creatorid = request.args.get('CREATORID', None)
    consumerid = request.args.get('CONSUMERID', None)
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


@app.route('/addsubscription')
def create_subscription():
    creatorid = request.args.get('CREATORID')
    consumerid = request.args.get('CONSUMERID')

    if (subscriptionLink.query.filter_by(CREATORID=creatorid, CONSUMERID=consumerid).first()):
        return jsonify(
            {
                "code": 400,
                "message": "Already subscribed."
            }
        ), 400

    created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    modified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    add = subscriptionLink(creatorid, consumerid, created, modified)

    try:
        db.session.add(add)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating subscription link"
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "message": "Subscription link created"
        }
    ), 201


if __name__ == '__main__':
    app.run(port=5001, debug=True)
