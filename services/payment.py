## Microservice to work with payment API ##

#import required modules
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/onlyfence'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Payment(db.Model):
    __tablename__ = 'payment_log'

    transactionid = db.Column(db.String(64), primary_key=True)
    consumerid = db.Column(db.String(64), nullable=False)
    creatorid = db.Column(db.String(64), nullable=False)
    payment_amount = db.Column(db.Float(precision=2), nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    modified = db.Column(db.DateTime, onupdate=datetime.now)


    def __init__(self, transactionid, consumerid, creatorid, payment_amount, transaction_date, modified):
        self.transactionid = transactionid
        self.consumerid = consumerid
        self.creatorid = creatorid
        self.payment_amount = payment_amount
        self.transaction_date = transaction_date
        self.modified = modified

    def json(self):
        return {"transactionid": self.transactionid, "consumerid": self.consumerid, "creatorid": self.creatorid, "payment_amount": self.payment_amount, "transaction_date": self.transaction_date, "modified": self.modified}

#get all payments (for testing)
@app.route("/payment")
def get_all():
    transactions = Payment.query.all()
    if len(transactions):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "books": [transaction.json() for transaction in transactions]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no transaction data."
        }
    ), 404

#invoke PayPal external transaction service (??????)

#create new payment record


if __name__ == '__main__':
    app.run(port=5001, debug=True)
