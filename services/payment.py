## Microservice to Log Payment information ##

import os, sys

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from invokes import invoke_http

# from crypt import methods
# from asyncio.windows_events import NULL
# import json
# import requests
# from invokes import invoke_http

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/payment'
#USE FOR DOCKER ONLY. UNCOMMENT THIS AND COMMENT OUT THE is213@localhost DATABASE URL WHEN USING DOCKER-------------------
#from os import environ
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#------------------------------------------------------------------------------------------
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

#get all payment logs (for testing)
@app.route("/payments")
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

# Create new payment record
@app.route("/payments/log", methods=['POST'])
# Receive HTTP request upon payment completion
def receiveLogRequest():
    if request.is_json: # Check if request data is in JSON format
        try: # Valid, Prepare Payment Log            
            transaction_id = request.json.get('TRANSACTIONID')
            creator_id = request.json.get('CREATORID')
            consumer_id = request.json.get('CONSUMERID')
            paymentamount = request.json.get('PAYMENTAMOUNT')

            paymentLog = Payment(
                transactionid=transaction_id, 
                consumerid=consumer_id, 
                creatorid=creator_id, 
                payment_amount=paymentamount, 
                transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                modified = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            try: # Upload to database
                db.session.add(paymentLog)
                db.session.commit()
            except Exception as e: 
                return jsonify(
                    {
                        "code": 500, 
                        "message": "An error occured creating Payment Log: " + str(e)
                    }
                ), 500 # Internal Server Error
            return jsonify(
                {
                    "code": 201,
                    "message": "Payment Logged"
                }
            ), 201 # Success
        except Exception as e: # Exception for error handling
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            print('Failed to log. Invalid JSON')
            return jsonify({
                "code": 400,
                "message": "Request should be in JSON. Error: " + ex_str
            }), 400 # Bad Request Input

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
