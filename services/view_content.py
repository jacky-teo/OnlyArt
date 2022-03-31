## Complex Microservice when consumer views content ##
from flask import Flask, request, jsonify
from flask_cors import CORS
from os import environ
import os
import sys

from invokes import invoke_http

import pika
import amqp_setup
import json

app = Flask(__name__)
CORS(app)

subscription_url =environ.get('subscription_url') or "http://localhost:5006/subscription/status"
creator_url =environ.get('creator_url') or "http://localhost:5002/creator/price"
unsubbed_url =environ.get('unsubbed_url') or "http://localhost:5003/unsubbed"
subbed_url =environ.get('subbed_url') or "http://localhost:5003/subbed"


@app.route("/view_content",methods=["POST","GET"])
def view_content():
    if request.is_json:
        try:
            creator_consumer = request.get_json()
            print(creator_consumer)
            result = view(creator_consumer)
            return(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "view_content.py internal error: " + ex_str
            }), 500
    else:
        return jsonify({
                "code": 400,
                "message": "no json was parsed or invalid json"
            }), 400



def view(creator_consumer):
    
    print('-----Invoking subscription_link microservice-----')
    subStatus = invoke_http(subscription_url, json=creator_consumer)
    
    subCode = subStatus["code"]
    message = subStatus["message"]
    # message = json.dumps(subStatus)

    if subCode not in range(200, 300):
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="view_content.subscription_status.error",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))

        return {
            "code": 500,
            "data": {"subStatus": subStatus},
            "message": "Failed to obtain subscription status"
        }

    else:
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="view_content.subscription_status.info",
                                         body=message)
    print(subStatus)
    subData = subStatus['data']
    print(subData["status"])
    subType = subData['isSubbed']

    print('-----Invoking creator_account microservice-----')
    creatorPrice = invoke_http(creator_url, json=subData["status"])
    print(creatorPrice)

    crCode = creatorPrice["code"]
    crData = creatorPrice

    if crCode not in range(200, 300):
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="view_content.creator_price.error",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))

        return {
            "code": 500,
            "data": {"creatorPrice": creatorPrice},
            "message": "Failed to obtain creator price."
        }
    else:
        amqp_setup.channel.basic_publish(
            exchange=amqp_setup.exchangename, routing_key="view_content.creator_price.info", body=message)

    if subType == 2:
        print('-----Retrieving content for unsubbed consumer-----')
        unsubbed = invoke_http(unsubbed_url, json=crData)

        conCode = unsubbed["code"]
        message = unsubbed["message"]

        if conCode not in range(200, 300):
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="view_content.unsubbed_content.error",
                                             body=message, properties=pika.BasicProperties(delivery_mode=2))

            return {
                "code": 500,
                "data": {"unsubbedContent": unsubbed},
                "message": "Failed to obtain unsubbed content"
            }
        else:
            amqp_setup.channel.basic_publish(
                exchange=amqp_setup.exchangename, routing_key="view_content.unsubbed_content.info", body=message)

        return unsubbed
    else:
        print('-----Retrieving content for subscriber-----')
        subbed = invoke_http(subbed_url, json=crData)
        conCode = subbed["code"]
        message = subbed["message"]

        if conCode not in range(200, 300):
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="view_content.subbed_content.error",
                                             body=message, properties=pika.BasicProperties(delivery_mode=2))

            return {
                "code": 500,
                "data": {"subbedContent": subbed},
                "message": "Failed to obtain subbed content"
            }
        else:
            amqp_setup.channel.basic_publish(
                exchange=amqp_setup.exchangename, routing_key="view_content.subbed_content.info", body=message)
        return subbed


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
