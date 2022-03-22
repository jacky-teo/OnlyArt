## Microservice to work with payment API ##

#import required modules
# from crypt import methods
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import requests
# from invokes import invoke_http

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/payment'
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

#invoke PayPal external transaction service (?????? - might be done by payment.js instead)
@app.route("/payments/capture", methods=['POST'])
def receiveCaptureRequest():
    # Check if the order contains valid JSON 
    if request.is_json:
        captureData = request.get_json()
        auth_token = getAuthorization()
        result = capturePayment(captureData, auth_token)
        return jsonify(result), result["code"]
    else:
        data = request.get_data()
        print("Received an invalid request:")
        print(data)
        return jsonify({"code": 400,
                        "data": str(data),
                        "message": "Request should be in JSON."}), 400 # Bad Request Input

def getAuthorization():
    print("--- Getting Authorization ---")
    client_id = "Afx50ZFn0R7g2tyN0P08kc3fBR0Csy8w1J25MND90MVCnpbLwiaIS-UiNElzqypPKulongQDAcq41D0M"
    client_secret = "EEyi_jCVZqhDRwq8gvtrh6hnJw6QPuNCGhXqUsLaNr99zeJxWYMwa3kOdM6tYrS8_IrkRT6mQFo8wZ1R"
    auth_URL = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    auth_payload = {'grant_type':'client_credentials'}
    authorization_response = requests.post(auth_URL, auth=(client_id,client_secret), data = auth_payload)
    
    if authorization_response.status_code != 200: 
        print("Failed to obtain token from the OAuth 2.0 server")
    else: 
        print("Successfully obtained a new token")
        tokens = json.loads(authorization_response.text)
        return tokens['access_token']

def capturePayment(captureData, auth_token):
    print("--- Requesting PayPal to capture the payment ---")
    print(captureData)

    return { 
        "code": "code",
        "data": {
            "status": "status"
        },
        "message": "message"
    }
    # data = request.get_json()
    # data = jsonify(data)
    # return data

#create new payment record (handle successful transactions)

# TESTING AUTHORIZATION
@app.route("/payments/auth", methods=['GET'])
def getAuthorization():
    print("--- Getting Authorization ---")
    client_id = "Afx50ZFn0R7g2tyN0P08kc3fBR0Csy8w1J25MND90MVCnpbLwiaIS-UiNElzqypPKulongQDAcq41D0M"
    client_secret = "EEyi_jCVZqhDRwq8gvtrh6hnJw6QPuNCGhXqUsLaNr99zeJxWYMwa3kOdM6tYrS8_IrkRT6mQFo8wZ1R"
    auth_URL = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    auth_payload = {'grant_type':'client_credentials'}
    authorization_response = requests.post(auth_URL, auth=(client_id,client_secret), data = auth_payload)
    
    if authorization_response.status_code != 200: 
        print("Failed to obtain token from the OAuth 2.0 server")
    else: 
        print("Successfully obtained a new token")
        tokens = json.loads(authorization_response.text)
        return tokens['access_token']

if __name__ == '__main__':
    app.run(port=5005, debug=True)
