import datetime
import os
import json
import requests
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import SignupForm, noaaDataForm
from models import Signups
from database import db_session
from utils import *
from noaaApi import NOAAData


def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

# app = Flask(__name__)
app = create_app()

app.secret_key = os.environ['APP_SECRET_KEY']
google_api_key = os.environ['GOOGLE_API_KEY']
noaa_api_key = os.environ['NOAA_API_KEY']



@app.route("/")
def index():
    return render_template('index.html')

# https://github.com/crvaden/NOAA_API_v2
@app.route("/noaaCategories", methods=('GET', 'POST'))
def noaaCategories():
    data = NOAAData(noaa_api_key)
    form = noaaDataForm()
    # if form.validate_on_submit():
    #     weather_data = data.fetch_data(datasetid='GHCND', locationid='ZIP:' + form.zipCode.data, startdate=form.startDate.data, enddate=form.endDate.data, limit=1000)
    # else:
    categories = data.data_categories(locationid='FIPS:37', sortfield='name')
    for i in categories:
        print(i)
    return render_template('noaa.html', form=form, noaaData=categories)

@app.route("/noaaWeatherData", methods=('GET', 'POST'))
def noaaWeatherData():
    data = NOAAData(noaa_api_key)
    form = noaaDataForm()
    payload = dict(datasetid='GHCND', locationid='ZIP:21113', startdate='2010-05-01', enddate='2010-05-02', limit=1000)
    if form.validate_on_submit():
        payload['locationid'] = "ZIP:" + form.zipCode.data
        print(payload)
    #     weather_data = data.fetch_data(datasetid='GHCND', locationid='ZIP:21113', startdate='2010-05-01', enddate='2010-05-02', limit=1000)
    weather_data = data.fetch_data(**payload)

    return render_template('noaa.html', form=form, noaaData=weather_data)



@app.route("/signup", methods=('GET', 'POST'))
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        signup = Signups(name=form.name.data, email=form.email.data, date_signed_up=datetime.datetime.now())
        db_session.add(signup)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('signup.html', form=form)

@app.route("/success")
def success():
    message = "Thank you!"
    return render_template('message.html', message=message)

@app.route("/map")
def locateMe():
    return render_template('map.html', google_api_key=google_api_key )

@app.route("/alerts")
def alertMe():
    res = getWeatherAlerts()
    if res.status_code == requests.codes.ok:
        res = res.json()
        features = res['features']
        return render_template('alerts.html', response=features )
    else:
        return render_template('error.html', response_code=res.status_code )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
