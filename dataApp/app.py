import datetime
import os
import json
import requests
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask import Response
from flask import request
#from forms import SignupForm, noaaDataForm
#from models import Signups
#from database import db_session
#from utils import *
#from noaaApi import NOAAData
#from google import *
import pandas as pd
import numpy as np
import dataprocess as csvData
from datetime import datetime


def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

# app = Flask(__name__)
app = create_app()

#fileName = "api_credentials.json"

#credentials = loadCreds(fileName)
#print(credentials)


app.secret_key = os.environ['APP_SECRET_KEY']
google_api_key = os.environ['GOOGLE_API_KEY']
noaa_api_key = os.environ['NOAA_API_KEY']

@app.route("/")
def index():
    state = request.args.get('state')
    # result = csvData.getStateRating("MARYLAND")
    currentMonth = datetime.now().month
    print("CURRENTMONTH: ", currentMonth)
    result = csvData.getPrediction(state, currentMonth)
    data = {
        'results'  : state,
        'number' : 0
    }
    data['number'] = int(result)
    js = json.dumps(data)
    # js = json.dumps(result)
    resp = Response(js, status=200, mimetype='application/json')
    #resp.headers['Link'] = 'http://placeholder.com'
    return resp

@app.route("/events")
def eventLocations():
    state = request.args.get('state')
    result = csvData.getStateEvents(state)
    data = {
        'location'  : state,
        'results' : result
    }
    # data['number'] = int(result)
    js = json.dumps(data)
    # js = json.dumps(result)
    resp = Response(js, status=200, mimetype='application/json')
    #resp.headers['Link'] = 'http://placeholder.com'
    return resp


@app.errorhandler(404)
def page_not_found(e):
    return ("Bad reques")
#return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5091, debug=True, use_reloader=False)
