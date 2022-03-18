from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from firebase_admin import storage


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/content'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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


class creatorContent(db.Model):
    __tablename__ = 'creator_content'
    POSTID = db.Column(db.String(13), primary_key=True)
    CREATORID = db.Column(db.String(64), nullable=False)
    DESCRIPTION = db.Column(db.String(64), nullable=False)
    IMAGE_ID = db.Column(db.String(64), nullable=False) ## Storing file directory
    POST_DATE = db.Column(db.DateTime, nullable=True, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=True,default=datetime.now, onupdate=datetime.now)

    def __init__(self, POSTID, CREATORID, DESCRIPTION, IMAGE_ID,POST_DATE,modified):
        self.POSTID = POSTID
        self.CREATORID = CREATORID
        self.DESCRIPTION = DESCRIPTION
        self.IMAGE_ID = IMAGE_ID
        self.POST_DATE = POST_DATE
        self.modified = modified

    def json(self):
        
        return {"POSTID": self.POSTID, "CREATORID": self.CREATORID, "DESCRIPTION": self.DESCRIPTION, "IMAGE_ID": self.IMAGE_ID,"POST_DATE": self.POST_DATE,"modified": self.modified}


@app.route("/content/<string:creatorID>")
def find_by_creatorID(creatorID):
    init_firebase()

    content_list = creatorContent.query.filter_by(CREATORID=creatorID)
    bucket = storage.bucket()
    blobs = list(bucket.list_blobs(prefix=f'{creatorID}/'))
    urls = []
    # upload via file
    for item in blobs[1:]:
        item.make_public()
        urls.append(item.public_url)

    if content_list:
        return jsonify({
            "code":200,
            "data":[content.json() for content in content_list],
            "urls":urls
        })
    return jsonify({
        "code":404,
        "message":"Content Not Found"
        }
    ),404  


@app.route("/unsubbed/<string:creatorID>")
def unsubbed(creatorID):
    init_firebase()

    content_list = creatorContent.query.filter_by(CREATORID=creatorID).limit(3)
    bucket = storage.bucket()
    blobs = list(bucket.list_blobs(prefix=f'{creatorID}/',max_results=4))
    urls = []
    # upload via file
    for item in blobs[1:]:
        item.make_public()
        urls.append(item.public_url)

    if content_list:
        return jsonify({
            "code":200,
            "data":[content.json() for content in content_list],
            "urls":urls
        })
    return jsonify({
        "code":404,
        "message":"Content Not Found"
        }
    ),404


@app.route("/upload", METHOD="POST")
def upload():
    init_firebase() ## Initiate firebase

    creatorID = request.args.get('creatorID',None) ## Get CreatorID
    description = request.args.get('description',None) ## Get Description
    file = request.files['file'] ## Request the file from the html
    filename = file.filename.split('.') ## Split the filename
    fileExtention = filename[-1] ## Get the extension

    bucket = storage.bucket() ## Get the storage in firebase
    blobs = list(bucket.list_blobs(prefix=f'{creatorID}/'))
    urls = [] #Create a place to store all the URLS
    
    # Append all the files in blobs to URL except parent file
    for item in blobs[1:]:
        item.make_public()
        urls.append(item.public_url)

    imageID = 'img'+ str(len(urls)+1) ## Create the Image ID based on the number of files inside the storage under creatorID

    path_on_cloud = f'{creatorID}/{imageID}.{fileExtention}' ##Declare the path to upload
    blob = bucket.blob(path_on_cloud) #Point to the path and the file name

    blob.upload_from_filename(file)  #Upload the file into the storate

    toUpload = creatorContent(CREATORID=creatorID,DESCRIPTION=description,IMAGE_ID=imageID) ## Create object to update sql

    try:
        db.session.add(toUpload) ## Update SQL
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while uploading the content. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": toUpload.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(port=5000, debug=True)
