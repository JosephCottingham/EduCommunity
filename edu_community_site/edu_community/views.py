from flask_login import logout_user, login_user
from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request
from .sql_models import User, Community
from .forms import *
from edu_community import sqlDB
appBlueprint = Blueprint('app',__name__)

@appBlueprint.route("/logout")
def logout():
    x = logout_user()
    print('user logout: ' + str(x))
    return redirect(url_for('app.home'))

@appBlueprint.route("/login", methods=['GET','POST'])
def login():
    login_form = Login_Form()
    signup_form = Signup_Form()

    if request.method == 'POST':
        if login_form.validate_on_submit() and login_form.login_submit.data:
            temp_user = sqlDB.session.query(User).filter_by(email=login_form.email.data).first()
            if temp_user and temp_user.check_password(login_form.password.data):
                login_user(temp_user)
                return redirect(url_for('app.home'))
            else:
                return 'error' #TODO ERROR Handling
        if signup_form.validate_on_submit() and signup_form.signup_submit.data:
            temp_user = sqlDB.session.query(User).filter_by(email=login_form.email.data).first()
            if not temp_user and signup_form.password.data == signup_form.password_confirm.data:
                new_user = User(email=signup_form.email.data, password=signup_form.password.data, name=signup_form.name.data)
                sqlDB.session.add(new_user)
                sqlDB.session.commit()
                login_user(new_user)
                return redirect(url_for('app.home'))
            else:
                return 'error' #TODO ERROR Handling

    return render_template('login.html',
    login_form=login_form,
    signup_form=signup_form
    )

@appBlueprint.route("/home")
def home():
    return render_template('home.html')

@appBlueprint.route("/create")
def create_community():
    community_create_form = Community_Create_Form()
    if request.method == 'POST':
        if community_create_form.validate_on_submit():
            if sqlDB.session.query(Community).filter_by(name=community_create_form.name).first():
                return 'error' #TODO ERROR Handling
            else:
                new_community = Community(name=community_create_form.name,
                dis=community_create_form.dis,
                owner=current_user)
                
    return render_template('create_community.html',
    community_create_form=community_create_form
    )


@appBlueprint.route("/c/<community_code>")
def community(community_code):
    temp_community = db.session.query(Community).filter_by(code=community_code).first_or_404()
    return redirect(url_for('app.community_text_channel', community_code=community_code, channel_code=temp_community.text_channels[0].code))

@appBlueprint.route("/c/<community_code>/t/<channel_code>")
def community_text_channel(community_code, channel_code):
    temp_community = db.session.query(Community).filter_by(code=community_code).first_or_404()
    temp_channel = temp_community.text_channels.filter_by(code=community_code).first_or_404()

    return render_template('/textchannel',
        community=temp_community,
        channel=temp_channel
    )
 

@appBlueprint.route("/")
def front():
    return render_template('front.html')
