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

upload_url = "http://localhost:5003/upload"
subscription_url = "http://localhost:5001/subscription/getsubscribers"
notification_url = "http://localhost:5002/notify/"


#Step 1 Upload the image & Upload information is returned (content.py)
# - 
#Step 2 Get list of people who subscribed to the creator to send out notification
#Step 3 Send information to Notifcation.py
#DONE

@app.route("/post_content")
def post_content():
    try: 
        uploadInformation = upload_content()
        telegramTags = getTelegramTags()
        return telegramTags
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

def upload_content():
    uploadInformation = invoke_http(upload_url)
    return uploadInformation

def getTelegramTags(uploadInformation):
    telegramTags = invoke_http(upload_url,json=uploadInformation)
    return telegramTags

def notifyUsers(uploadInformation,telegramTags):
    notification_status = None
    return notification_status

if __name__ == "__main__":
    app.run(port=5100, debug=True)