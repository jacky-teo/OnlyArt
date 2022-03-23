## Complex Microservice when consumer wants to subscribe to a creator ##

from distutils.log import error
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from itsdangerous import json       #not sure how to use this module (copy pasted from labs) but fyi its for security purposes
import requests
from invokes import *
#import amqp_setup
#import pika
import json
app = Flask(__name__)
CORS(app)

#creator_URL = "http://localhost:5002/creator/price"
#payment_URL = "http://localhost:5005/payments/capture"
sub_link_URL ="http://localhost:5006/subscription/status"
make_subscription_URL ="http://localhost:5006/subscription/add"

#app handles incoming HTTP request
@app.route("/make_subscription", methods=['POST','GET'])
def attempt_sub():
    #check if input data is valid and if request data is in json format
    if request.is_json:
        try: 
            #input data correct, call processSubscription function
            attempt = request.get_json()
            print("\nReceived an attempt in JSON:", attempt)
            answer = processSubscription(attempt)
            return answer



            #try
        except Exception as e:
            #exception for error handling
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            print('shit')
            return jsonify({
                        "code": 500,
                        "message": "FAILURE, EMOTIONAL DAMAGE " 
                    }) #return error response if input invalid
def processSubscription(attempt):
    #THE AGE OF VERIFICATION COMETH
    #Sends a verification check to sub link microservice to find if consumer has already subbed to the creator
    print('\n-----Invoking subscriber link check microservice-----')
    subscribe_result = invoke_http(sub_link_URL,method="GET", json=attempt)
    print('subscribe_result:', subscribe_result)

    is_subbed = subscribe_result["isSubbed"]
    code = subscribe_result["code"]
    message = json.dumps(subscribe_result) 

    #amqp_setup.check_setup() stopped temporarily

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (subscribe error) message with routing_key=subscribe.error-----')


        # {amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="subscribe.error", 
        #    body=message, properties=pika.BasicProperties(delivery_mode = 2)) } stopped temporarily

        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails    
        # {:d} means the result will be a decimal interger    
        print("\nSubscribe status ({:d}) published to the RabbitMQ Exchange:".format(
            code), subscribe_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"subscribe_result": subscribe_result},
            "message": "Subcribe failure sent for error handling."
        }
    elif is_subbed == 1:
        # Inform the error microservice
        print('\n\n-----Publishing the (subscribe error) message with routing_key=subscribe.error-----')



        # {amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="subscribe.error", 
        #    body=message, properties=pika.BasicProperties(delivery_mode = 2)) } stopped temporarily
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails    
        # {:d} means the result will be a decimal interger    
        print("\nSubscribe status ({:d}) published to the RabbitMQ Exchange:".format(
            code), subscribe_result)
        return {
            "code": 500,
            "message": "Subcribe failure sent for error handling.",
            "Consumer message": "Failure... you already sub lah"
        }
    else:
        #Send command to payment microservice to process payment. (TO BE DONE)

        # 4. Record new order
        # record the activity log anyway
        #print('\n\n-----Invoking activity_log microservice-----')
        return {"message":"IT LIVES" }
        #print('\n\n-----Publishing the (subscribe info) message with routing_key=subscribe.info-----')        

        # invoke_http(activity_log_URL, method="POST", json=order_result)            
        #amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="subscribe.info", 
        #    body=message)
        
if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5101, debug=True)        
    
    
        





#function that invokes microservices to handle request
