## Microservice to work with telegram API ##
import requests
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/notification'  #For Mac
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/notification'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
token = os.getenv('TELEGRAM_KEY')

db = SQLAlchemy(app)

class Notification(db.Model):
    __tablename__ = 'notification'

    chatid = db.Column(db.String(64), primary_key=True)
    telegramtag = db.Column(db.String(64), nullable=False)

    def __init__(self, chatid, telegramtag):
        self.chatid = chatid
        self.telegramtag = telegramtag

    def json(self):
        return {"chatid": self.chatid, "telegramtag": self.telegramtag}


@app.route("/chat")
def get_all():
    chatlist = Notification.query.all()
    if len(chatlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "chats": [chat.json() for chat in chatlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no chat ids."
        }
    ), 404


@app.route("/chat/<string:telegramtag>")
def find_by_isbn13(telegramtag):
    notif = Notification.query.filter_by(telegramtag=telegramtag).first()
    if notif:
        return jsonify(
            {
                "code": 200,
                "data": notif.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Notification information not found."
        }
    ), 404


@app.route("/chat/<string:telegramtag>", methods=['POST'])
def create_notif(telegramtag):
    if (Notification.query.filter_by(telegramtag=telegramtag).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "telegramtag": telegramtag
                },
                "message": "Notification info already exists."
            }
        ), 400

    data = request.get_json()
    print(data['chatid'])
    notif = Notification(data['chatid'],telegramtag)

    try:
        db.session.add(notif)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "telegramtag": telegramtag
                },
                "message": "An error occurred creating the notif."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": notif.json()
        }
    ), 201

@app.route("/notify/<string:creatorname>",methods=["POST",'GET'])
def send_notif(creatorname):
    #some function here
    countnotif = 0
    #json sent is a list of telegram tags to be notified
    data = request.get_json()
    #print("creatorname: ",creatorname)
    #print("data: ",data)
    notiflist = data["data"]
    print(notiflist)
    #print("NL: ",notiflist)
    for user in notiflist:
        #request send
        #print("user: ",user)
        if (Notification.query.filter_by(telegramtag=user).first()):
            notif = Notification.query.filter_by(telegramtag=user).first()
            notifinfo = notif.json()
            chatid = notifinfo["chatid"]
            #print("chatid: ",chatid)
            chatmsg = "Creator " + creatorname + " has posted! Check it out on OnlyFences now!"
            #chatparams = {'chat_id': chatid , 'text': chatmsg}
            sendurl = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chatid + "&text=" + chatmsg 
            r = requests.get(sendurl)
            countnotif += 1
    if countnotif == 0:        
        return jsonify(
                {
                    "code": 500,
                    "message": "Notification was unsuccessful. No notifs sent."
                }
            ), 500
    else:
        successmsg = "Notification was successful." + str(countnotif) + " number of notifs were sent."
        return jsonify(
                {
                    "code": 201,
                    "message": successmsg
                }
            ), 201


if __name__ == '__main__':
     app.run(host='127.0.0.1', port=5000, debug=True)
