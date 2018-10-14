import datetime
import os
import json
import requests
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import SignupForm
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
@app.route("/noaa")
def index():
    data = NOAAData(noaa_api_key)

    categories = data.data_categories(locationid='FIPS:37', sortfield='name')

    # for i in categories:
    #     print(i)
    return render_template('noaa.html', categories=categories)


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
