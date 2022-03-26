## Complex Microservice when creator post a content ##
## Complex Microservice when consumer views content ##
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import storage
import os, sys
from datetime import datetime
from invokes import invoke_http
from firebase import init_firebase,upload_firebase

# import amqp_setup
# import pika
import json

app = Flask(__name__)
CORS(app)

upload_url = "http://localhost:5003/upload"
subscription_url = "http://localhost:5006/subscription/getsubscribers"
notification_url = "http://localhost:5000/notify/"
creator_url = "http://localhost:5002/creator/getinfo/"

#Step 1 Upload the image & Upload information is returned (content.py)
# - 
#Step 2 Get list of people who subscribed to the creator to send out notification
#Step 3 Send information to Notifcation.py
#DONE

@app.route("/post_content",methods=['GET','POST'])
def post_content():
    init_firebase() ## Initiate firebase
    if request.method =="POST": ## Check if method is POST before proceeding
        file = request.files['file'] ## Get the file to be uploaded
        creatorID= request.form['creatorID'] ## Get the CreatorID from form
        description = request.form['description']  ## Get the description from form

    data = upload_firebase(file,creatorID,description)
    data_json =  json.dumps(data) 
    try: 
        upload_content(data_json) # Upload image into firebase and it goes to SQL
        creatorID_JSON = json.dumps({"CREATORID":creatorID}) ## Add creatorID as a json file
        consumerTelegram = telegramTags(creatorID_JSON) ## Get all the followers that are subscribed to creator
        creatorinfo= creatorInformation(creatorID)# Get creator information
        creatorname = creatorinfo['data']['username'] #Get creator name to use for notification status
        notifyStatus = notifyUsers(consumerTelegram,creatorname) #notify users
        return notifyStatus # returns notification to users

    except Exception as e:
                # Unexpected error in code
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
                print(ex_str)

                return jsonify({
                    "code": 500,
                    "message": "post_content internal error: " + ex_str
                }), 500

def upload_content(json): 
    uploadInformation = invoke_http(upload_url,method='POST',json=json)
    if uploadInformation['code'] not in range(200,300):
        return {
            "code": 500,
            "data": {"uploadInformation":uploadInformation},
            "message": "Failed to upload image"
        }  
    return uploadInformation


def telegramTags(uploadInformation): 
    tags = invoke_http(subscription_url,method="GET",json=uploadInformation)
    if tags['code'] not in range(200,300):
        return {
            "code": 500,
            "data": {"tags":tags},
            "message": "Failed to retrieve subscribers"
        }  
    return tags

def notifyUsers(tags,creatorname):
    
    notification_status = invoke_http(f"{notification_url}{creatorname}",json=tags)
    if notification_status['code'] not in range(200,300):
        return {
            "code": 500,
            "data": {"notification_status":notification_status},
            "message": "Failed to notify users"
        }
    return notification_status

def creatorInformation(creatorID):
    info = invoke_http(f'{creator_url}{creatorID}')
    return info

if __name__ == "__main__":
    app.run(port=5100, debug=True)