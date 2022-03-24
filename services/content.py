from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from firebase_admin import storage
import json
from firebase import delete_firebase,update_firebase

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


class Content(db.Model):
    __tablename__ = 'content'
    POSTID = db.Column(db.String(13), primary_key=True)
    CREATORID = db.Column(db.String(64), nullable=False)
    DESCRIPTION = db.Column(db.String(64), nullable=False)
    IMAGE_ID = db.Column(db.String(64), nullable=False) ## Storing imageID for firebase
    IMG_EXT = db.Column(db.String(64), nullable=False)
    POST_DATE = db.Column(db.DateTime, nullable=True, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=True,default=datetime.now, onupdate=datetime.now)

    def __init__(self, POSTID, CREATORID, DESCRIPTION, IMAGE_ID,IMG_EXT,POST_DATE,modified):
        self.POSTID = POSTID
        self.CREATORID = CREATORID
        self.DESCRIPTION = DESCRIPTION
        self.IMAGE_ID = IMAGE_ID
        self.IMG_EXT = IMG_EXT
        self.POST_DATE = POST_DATE
        self.modified = modified

    def json(self):
        
        return {"POSTID": self.POSTID, "CREATORID": self.CREATORID, "DESCRIPTION": self.DESCRIPTION, "IMAGE_ID": self.IMAGE_ID,"IMG_EXT":self.IMG_EXT,"POST_DATE": self.POST_DATE,"modified": self.modified}


@app.route("/subbed")
def find_by_creatorID():
    data = request.get_json()
    creatorID = data["CREATORID"]
    init_firebase() # initialize firebase

    content_list = Content.query.filter_by(CREATORID=creatorID)
    bucket = storage.bucket()
    blobs = list(bucket.list_blobs(prefix=f'{creatorID}/'))
    urls = [] # used later to store urls
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


@app.route("/unsubbed") ## My unsub is broken T____T
def unsubbed():
    data = request.get_json()
    creatorID = data["CREATORID"]
    init_firebase()

    content_list = Content.query.filter_by(CREATORID=creatorID).limit(3)
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


@app.route("/upload",methods=['POST','GET'])
def upload():
    data = request.get_json()
    data = json.loads(data)
    postID,creatorID,description,imageID,imageEXT = data['POSTID'],data['CREATORID'],data['DESCRIPTION'],data['IMAGE_ID'],data['IMG_EXT']
    toUpload = Content(POSTID=postID,CREATORID=creatorID,DESCRIPTION=description,IMAGE_ID=imageID,IMG_EXT=imageEXT,POST_DATE=None,modified=None) ## Create object to update sql
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

@app.route("/delete/<string:postID>",methods=['POST','GET','DELETE'])
def delete(postID):
    init_firebase() ## Initiate firebase
    # creatorID,imageID= postID.split('_')
    ## Get postID information from Database
    content = Content.query.filter_by(POSTID=postID).first()
    ## Get Creator ID
    if content:
        data = content.json()
        if data['IMG_EXT']:
            fileEXT = data['IMG_EXT']
            delete_firebase(postID,fileEXT)

        db.session.delete(content)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "PostID": postID
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "PostID": postID
            },
            "message": "Content not found."
        }
    ), 404
        
@app.route("/update/<string:postID>", methods=['PUT','POST'])
def update(postID):
    content = Content.query.filter_by(POSTID=postID).first()
    information = content.json()
    if content:
        imageID =f"{information['imageID']}"
        if data['IMAGE_ID']:
            creatorID=data['CREATORID']
            file = request.files['file'] #Get file from HTML post request
            if file:
                fileEXT = file.mimetype.split('/')[1]
                update_firebase(creatorID,imageID,file,fileEXT)

        data = request.get_json()
        if data['DESCRIPTION']:
            content.DESCRIPTION = data['DESCRIPTION']

        content.modified = datetime.now()

        
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": content.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "postID": postID
            },
            "message": "Book not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5003, debug=True)
