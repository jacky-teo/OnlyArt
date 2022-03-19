## Complex Microservice when consumer wants to subscribe to a creator ##

from distutils.log import error
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from itsdangerous import json       #not sure how to use this module (copy pasted from labs) but fyi its for security purposes

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

creator_URL = ""
payment_URL = ""
sub_link_URL = ""

#app handles incoming HTTP request
@app.route("/place_order", methods=['POST'])
def place_order():
    #check if input data is valid and if request data is in json format
    if request.is_json:
        try: 
            #input data correct, call processSubscription function
            print('called')

            #try
        except Exception as e:
            #exception for error handling
            print('shit')

    #return error response if input invalid



#function that invokes microservices to handle request
def processSubscription():
    print('Processing subscription')