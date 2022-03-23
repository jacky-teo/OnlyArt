## Complex Microservice when creator post a content ##
## Complex Microservice when consumer views content ##
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

from invokes import invoke_http

# import amqp_setup
# import pika
import json

app = Flask(__name__)
CORS(app)

subscription_url = "http://localhost:5001/subscription/status"
creator_url = "http://localhost:5002/creator/price"
upload_url = "http://localhost:5003/upload"

#Step 1 Upload the image & Upload information is returned (content.py)
# - 
#Step 2 Get list of people who subscribed to the creator to send out notification
#Step 3 Send information to Notifcation.py
#DONE

@app.route("/post_content")
def post_content():
    if request.is_json:
        try: 
            creator_consumer = request.get_json()
            result = getStatus(creator_consumer)
            return(result)

        except Exception as e:
                    # Unexpected error in code
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
                    print(ex_str)

                    return jsonify({
                        "code": 500,
                        "message": "view_content.py internal error: " + ex_str
                    }), 500

def getStatus(creator_consumer):
    subStatus = invoke_http(subscription_url, json=creator_consumer)

    subCode = subStatus["code"]
    subMsg = json.dumps(subStatus["message"])
    subData = subStatus['data']

    if subCode not in range(200, 300):
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
        #     body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        return {
            "code": 500,
            "data": {"subStatus": subStatus},
            "message": "Failed to obtain subscription status"
        }    
    # else:          
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info", 
        #     body=message)
     
    creatorPrice = invoke_http(creator_url, json=subData)
    
    crCode = creatorPrice["code"]
    crData = creatorPrice["data"]
    
    if crCode not in range(200, 300):
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
        #     body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        return {
            "code": 500,
            "data": {"creatorPrice": creatorPrice},
            "message": "Failed to obtain creator price."
        }    
    # else:          
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info", 
        #     body=message)
    
    unsubbed = invoke_http(unsubbed_url, json=crData)
    return unsubbed



if __name__ == "__main__":
    app.run(port=5100, debug=True)