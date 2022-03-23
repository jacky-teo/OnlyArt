## Complex Microservice when consumer wants to subscribe to a creator ##

from distutils.log import error
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from itsdangerous import json       #not sure how to use this module (copy pasted from labs) but fyi its for security purposes
import requests
from invokes import *
import amqp_setup
import pika
import json
import amqp_setup
#NEED CONSUMER ID + PAYPAL EMAIL
app = Flask(__name__)
CORS(app)

creator_URL = "http://localhost:5002/creator/price"
add_subscription_URL ="http://localhost:5006/subscription/add"


#app handles incoming HTTP request
@app.route("/subscribe", methods=['POST', 'GET'])
def create_subscription():
    #check if input data is valid and if request data is in json format
    if request.is_json:
        try: 
            #input data correct, call processSubscription function
            attempt = request.get_json()
            print("\nReceived a request to subscribe in JSON:", attempt)
            result = processSubscription(attempt)
            return result

        except Exception as e:
            #exception for error handling
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            print('Failed to subscribe')
            return jsonify({
                "code": 500,
                "message": "subscribe.py internal error: " + ex_str
            }), 500 #return error response if input invalid


def processSubscription(attempt):
    #Verify if consumer has already subscribed through subscription link
    print('\n-----Invoking subscriber link check microservice-----')
    subscribe_result = invoke_http(creator_URL, method="GET", json=attempt)
    print('subscribe_result:', subscribe_result)

    
    code = subscribe_result["code"]
    message = json.dumps(subscribe_result) 

    amqp_setup.check_setup()

    #Check subscribe_result. If error, send error message to error.py and return error
    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (subscribe error) message with routing_key=subscribe.error-----')

        #route error message to error microservice
        {amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="subscribe.error", body=message, properties=pika.BasicProperties(delivery_mode = 2)) }

        # - reply from the invocation is not used;
        # continue even if this invocation fails    
        print("\nSubscribe status ({:d}) published to the RabbitMQ Exchange:".format(
            code), subscribe_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"subscribe_result": subscribe_result},
            "message": "Subcribe failure sent for error handling."
        }


    #consumer not subscribed to creator. proceed with subscription payment
    else:
        #retrieve payment details through creator_account microservice
        
        #redirect consumer to payment.html to initiate payment


        # 4. Record new order
        # record the activity log anyway
        #print('\n\n-----Invoking activity_log microservice-----')
        data = subscribe_result['data']
        price = data['PRICE']

        print(price)
        creatorID = data['CREATORID']
        email = data['EMAIL']
        return {
                "code": 200,
                "price": price,
                "creatorID" : creatorID ,
                "creatorEmail": email
            }
        #send json to UI


        #print('\n\n-----Publishing the (subscribe info) message with routing_key=subscribe.info-----')        

        # invoke_http(activity_log_URL, method="POST", json=order_result)            
        #amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="subscribe.info", body=message, properties=pika.BasicProperties(delivery_mode = 2))

@app.route("/confirmSubscription", methods = ['GET', 'POST'])
#function that passes in result from PayPal service after payment processed
def confirmPayment():
    print('\n Check if payment was processed successfully')
    #check if input data is valid and if request data is in json format
    if request.is_json:
        try: 
            #input data correct, call processSubscription function
            attempt = request.get_json()
            print("\nReceived a request to subscribe in JSON:", attempt)
            result = invoke_http(add_subscription_URL, method='POST', json =attempt)
            return result

        except Exception as e:
            #exception for error handling
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            print('Failed to subscribe')
            return jsonify({
                "code": 500,
                "message": "subscribe.py internal error: " + ex_str
            }), 500 
    #return error response if input invalid
    #receive JSON from UI
    #update subscription link
    #thank you page
        
if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5101, debug=True)        
    
