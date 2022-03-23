## Complex Microservice when creator post a content ##
## Complex Microservice when consumer views content ##
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import storage
import os, sys
from datetime import datetime
from invokes import invoke_http

# import amqp_setup
# import pika
import json

app = Flask(__name__)
CORS(app)

PROJECT_ID = 'onlyfence-9eb40'
IS_EXTERNAL_PLATFORM = True
firebase_app = None

def init_firebase():
    global firebase_app
    if firebase_app:
        return firebase_app

    import firebase_admin
    from firebase_admin import credentials
    if IS_EXTERNAL_PLATFORM:
        cred = credentials.Certificate('keys/firebase-adminsdk.json')
    else:
        cred = credentials.ApplicationDefault()

    firebase_app = firebase_admin.initialize_app(cred, {
        # 'projectId': PROJECT_ID,
        'storageBucket': f"{PROJECT_ID}.appspot.com"
    })

    return firebase_app

upload_url = "http://localhost:5003/upload"
subscription_url = "http://localhost:5006/subscription/getsubscribers"
notification_url = "http://localhost:5000/notify/"


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
    bucket = storage.bucket() ## Get the storage in firebase
    blobs = list(bucket.list_blobs(prefix=f'{creatorID}/')) #Point to creator's directory
    urls = [] #Create a place to store all the URLS
    url_links =[]# Append all the links in blobs to URL except parent file

    # Append all the files in blobs to URL except parent file
    for item in blobs[1:]: 
        item.make_public() #Get a session url that is public
        urls.append(item.public_url) #Get a session url that is public
        url_links.append(item.path) #Get the url pathing

    lastImgID = None  #Declared to use image naming
    for url in url_links: 
        url = url.lower() 
        id = url.split("f")[2] #Declared split the path by f
        lastImgID =id  #Assign image ID
    
    if lastImgID != None: #If its not none,

    # ['img1.png', 'img3.png']
        lastImgID = lastImgID.replace('img','')
        lastImgID = lastImgID.replace('.png','')
        imageID = 'img'+ str(int(lastImgID)+1)## Create the Image ID based on the number of files inside the storage under creatorID
    else:
        imageID = 'img1'

    postID = f'{creatorID}_{imageID}' #Create a post id
    fileEXT = file.mimetype.split('/')[1]

    path_on_cloud = f'{creatorID}/{imageID}.{fileEXT}' ##Declare the path to upload
    blob = bucket.blob(path_on_cloud) #Point to the path and the file name

    blob.upload_from_file(file,content_type = file.mimetype)  #Upload the file into the storate
    
    data = {
        'POSTID':postID,
        'CREATORID':creatorID,
        'DESCRIPTION':description,
        'IMAGE_ID':imageID,
        'IMG_EXT':fileEXT,
        'POST_DATE':None,
        'modified':None,
    } #Create a data to transfer as json
    data_json =  json.dumps(data) #Convert to JSON
    try: 
        uploadInformation = upload_content(data_json)
        telegramTags = invoke_http(subscription_url,json=uploadInformation)
        return telegramTags

    except Exception as e:
                # Unexpected error in code
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
                print(ex_str)

                return jsonify({
                    "code": 500,
                    "message": "post_content.py internal error: " + ex_str
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




def notifyUsers(uploadInformation,telegramTags):
    notification_status = None
    return notification_status

if __name__ == "__main__":
    app.run(port=5100, debug=True)