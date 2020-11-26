from flask_login import logout_user, login_user
from flask import Flask, render_template, redirect, url_for, Blueprint, flash
from .models import User, Community
from ballotSite import db
appBlueprint = Blueprint('app',__name__)

@appBlueprint.route("/logout")
def logout():
    x = logout_user()
    print('user logout: ' + str(x))
    return redirect(url_for('app.home'))

@appBlueprint.route("/")
def home():
    return render_template('home.html')
