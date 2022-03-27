## Complex Microservice when consumer wants to subscribe to a creator ##

from distutils.log import error
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
# from itsdangerous import json       #not sure how to use this module (copy pasted from labs) but fyi its for security purposes
import requests
from invokes import *
import pika
import json
# import amqp_setup

app = Flask(__name__)
CORS(app)

creator_URL = "http://localhost:5002/creator/price"
add_subscription_URL ="http://localhost:5006/subscription/add"

# app handles incoming HTTP request
@app.route("/subscribe", methods=['POST'])
def check_request():
    # Check if input data is valid and if request data is in json format
    if request.is_json:
        try: 
            #input data correct, call processSubscription function
            attempt = request.get_json()
            print("Received a request to subscribe in JSON:", attempt)
            result = retrieveCreatorInformation(attempt)
            return result

        except Exception as e:
            #exception for error handling
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            print('Failed to subscribe. Invalid JSON')
            return jsonify({
                "code": 400,
                "message": "Request should be in JSON. Error: " + ex_str
            }), 400 # Bad Request Input


def retrieveCreatorInformation(attempt):
    # Pull creator information from creator_account
    print('-----Invoking creator_account microservice-----')
    retrieveInfo = invoke_http(creator_URL, method="GET", json=attempt)
    print('information_request:', retrieveInfo)
    
    code = retrieveInfo["code"]
    # message = json.dumps(retrieveInfo) 

    # amqp_setup.check_setup()

    # Check HTTP request. 
    if code not in range(200, 300): # Error!
        # # Inform the error microservice
        # print('\n\n-----Publishing the error message with routing_key=subscribe.error-----')

        # # Route error message to error microservice
        # {amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="subscribe.error", body=message, properties=pika.BasicProperties(delivery_mode = 2)) }

        # # - reply from the invocation is not used;
        # # continue even if this invocation fails    
        # print("\nStatus ({:d}) published to the RabbitMQ Exchange:".format(
        #     code), creator_information)

        # 7. Return error
        return {
            "code": 500,
            "data": {"retrieveInfo": retrieveInfo},
            "message": "Request failure sent for error handling."
        }

    else: # Success! 
        # Retrieve payment details through creator_account microservice
        
        data = retrieveInfo['data']
        price = data['PRICE']

        print(price)
        creatorID = data['CREATORID']
        creatorUsername = data['USERNAME']
        email = data['EMAIL']
        return {
                "code": 200,
                "price": price,
                "creatorID" : creatorID ,
                "creatorEmail": email,
                "creatorUsername": creatorUsername
            }

        # Update Activity AMQP 
        # invoke_http(activity_log_URL, method="POST", json=order_result)            
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="subscribe.info", body=message, properties=pika.BasicProperties(delivery_mode = 2))

@app.route("/confirmSubscription", methods = ['POST'])
# Function that passes in result from PayPal service after payment processed
def confirmPayment():
    print('Checking if payment was processed successfully...')
    #check if input data is valid and if request data is in json format
    if request.is_json:
        try: 
            #input data correct, call processSubscription function
            attempt = request.get_json()
            print("Received a request to link subscription in JSON:", attempt)
            subscriptionLinkResult = updateSubscriptionLink(attempt)
            print("Subscription Link Status: " + result['code'] + ": " + result['message'])
            return subscriptionLinkResult

        except Exception as e:
            #exception for error handling
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            print('Failed to subscribe. Invalid JSON')
            return jsonify({
                "code": 400,
                "message": "Request should be in JSON. Error: " + ex_str
            }), 400 
    #return error response if input invalid
    #receive JSON from UI
    #update subscription link
    #thank you page

def updateSubscriptionLink(data):
    print('Updating Subscription Link service...')

    # consumerID = data['CONSUMERID']
    # creatorID = data['CREATORID']
    prepJSON = {
        "CONSUMERID": data['CONSUMERID'],
        "CREATORID": data['CREATORID']
    }
    result = invoke_http(add_subscription_URL, method='POST', json=prepJSON)

    return result

        
if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5101, debug=True)        
    
