from pickle import TRUE
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/onlyfence'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class creatorContent(db.Model):
    __tablename__ = 'creator_content'
    POSTID = db.Column(db.String(13), primary_key=True)
    CREATORID = db.Column(db.String(64), nullable=False)
    DESCRIPTION = db.Column(db.String(64), nullable=False)
    IMAGE_URL = db.Column(db.String(64), nullable=False) ## Storing file directory
    POST_DATE = db.Column(db.DateTime, nullable=True, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=True,default=datetime.now, onupdate=datetime.now)

    def __init__(self, POSTID, CREATORID, DESCRIPTION, IMAGE_URL,POST_DATE,modified):
        self.POSTID = POSTID
        self.CREATORID = CREATORID
        self.DESCRIPTION = DESCRIPTION
        self.IMAGE_URL = IMAGE_URL
        self.POST_DATE = POST_DATE
        self.modified = modified

    def json(self):
        
        return {"POSTID": self.POSTID, "CREATORID": self.CREATORID, "DESCRIPTION": self.DESCRIPTION, "IMAGE_URL": self.IMAGE_URL,"POST_DATE": self.POST_DATE,"modified": self.modified}


@app.route("/creator_content")
def get_all():
    content_list = creatorContent.query.all()
    if len(content_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "contents": [content.json() for content in content_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no content."
        }
    ), 404

@app.route("/creator_content/<string:creatorID>")
def find_by_creatorID(creatorID):
    content_list = creatorContent.query.filter_by(CREATORID=creatorID)
    print(content_list)
    if content_list:
        return jsonify({
            "code":200,
            "data":[content.json() for content in content_list]
        })
    return jsonify({
        "code":404,
        "message":"Content Not Found"
        }
    ),404  

@app.route("/creator_content/upload")
def upload_content():
    data = request.get_json()
    content = creatorContent(**data)
    try:
        db.session.add(content)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the content. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": content.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(port=5000, debug=True)
