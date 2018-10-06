import datetime
import os
import requests
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import SignupForm
from models import Signups
from database import db_session
from utils import *


def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

# app = Flask(__name__)
app = create_app()

app.secret_key = os.environ['APP_SECRET_KEY']
google_api_key = os.environ['GOOGLE_API_KEY']


@app.route("/", methods=('GET', 'POST'))
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
    return "Thank you for signing up!"

@app.route("/map")
def locateMe():
    return render_template('map.html', google_api_key=google_api_key )

@app.route("/alerts")
def alertMe():
    response = getWeatherAlerts()
    return render_template('alerts.html', response=response )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
