## Complex Microservice when consumer views content ##
from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys

from invokes import invoke_http

import pika
import amqp_setup
import json

app = Flask(__name__)
CORS(app)

subscription_url = "http://localhost:5006/subscription/status"
creator_url = "http://localhost:5002/creator/price"
unsubbed_url = "http://localhost:5003/unsubbed"
subbed_url = "http://localhost:5003/subbed"


@app.route("/view_content")
def view_content():
    if request.is_json:
        try:
            creator_consumer = request.get_json()
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


def view(creator_consumer):
    subStatus = invoke_http(subscription_url, json=creator_consumer)

    subCode = subStatus["code"]
    subMsg = json.dumps(subStatus["message"])
    subData = subStatus['data']
    subType = subStatus['isSubbed']
    message = subMsg

    if subCode not in range(200, 300):
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="view.error",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))

        return {
            "code": 500,
            "data": {"subStatus": subStatus},
            "message": "Failed to obtain subscription status"
        }
    else:
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="view.info",
                                         body=message)

    creatorPrice = invoke_http(creator_url, json=subData)

    crCode = creatorPrice["code"]
    crData = creatorPrice["data"]

    if crCode not in range(200, 300):
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="view.error",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))

        return {
            "code": 500,
            "data": {"creatorPrice": creatorPrice},
            "message": "Failed to obtain creator price."
        }
    else:
        amqp_setup.channel.basic_publish(
            exchange=amqp_setup.exchangename, routing_key="view.info", body=message)

    if subType == 2:
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
    app.run(port=5100, debug=True)
