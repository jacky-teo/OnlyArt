from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class CREATOR_CONTENT(db.Model):
    __tablename__ = 'CREATOR_CONTENT'

    POSTID = db.Column(db.String(13), primary_key=True)
    CREATORID = db.Column(db.String(64), nullable=False)
    DESCRIPTION = db.Column(db.Float(precision=2), nullable=False)
    IMAGE = db.Column(db.BLOB(length=None), nullable=False)
    POST_DATE = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False,default=datetime.now, onupdate=datetime.now)

    def __init__(self, POSTID, CREATORID, DESCRIPTION, IMAGE,POST_DATE,modified):
        self.POSTID = POSTID
        self.CREATORID = CREATORID
        self.DESCRIPTION = DESCRIPTION
        self.IMAGE = IMAGE
        self.POST_DATE = POST_DATE
        self.modified = modified

    def json(self):
        return {"POSTID": self.POSTID, "CREATORID": self.CREATORID, "DESCRIPTION": self.DESCRIPTION, "IMAGE": self.IMAGE,"POST_DATE": self.POST_DATE,"modified": self.modified}


@app.route("/creator_content")
def get_all():
    content_list = CREATOR_CONTENT.query.all()
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


@app.route("/creator_content/<string:creatorid>")
def find_by_creatorid(creatorid):
    content_list = CREATOR_CONTENT.query.filter_by(creatorid=creatorid).first()
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
            "message": "There are no content for this creator."
        }
    ), 404


@app.route("/creator_content/<string:creatorid>", methods=['POST'])
def upload_content(creatorid):

    data = request.get_json()
    content = CREATOR_CONTENT(**data)

    try:
        db.session.add(content)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "CreatorID": creatorid
                },
                "message": "An error occurred inserting the content."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": content.json()
        }
    ), 201


@app.route("/content_creator/<string:contentID>", methods=['PUT'])
def update_content(contentID):
    content = CREATOR_CONTENT.query.filter_by(contentID=contentID).first()
    if content:
        data = request.get_json()
        if data['IMAGE']:
            content.IMAGE = data['IMAGE']
        if data['DESCRIPTION']:
            content.DESCRIPTION = data['DESCRIPTION']
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
                "contentID": contentID
            },
            "message": "Content not found."
        }
    ), 404


@app.route("/content_creator/<string:contentID>", methods=['DELETE'])
def delete_book(contentID):
    book = CREATOR_CONTENT.query.filter_by(contentID=contentID).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "contentID": contentID + ' has been deleted'
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "contentID": contentID
            },
            "message": "Content not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)
