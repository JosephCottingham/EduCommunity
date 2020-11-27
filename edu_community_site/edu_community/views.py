from flask_login import logout_user, login_user, current_user, login_required
from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request
from .sql_models import *
from .forms import *
from edu_community import sqlDB
appBlueprint = Blueprint('app',__name__)

@login_required
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
                login_user(sqlDB.session.query(User).get(new_user.id))
                return redirect(url_for('app.home'))
            else:
                return 'error' #TODO ERROR Handling

    return render_template('login.html',
    login_form=login_form,
    signup_form=signup_form
    )

@login_required
@appBlueprint.route("/home")
def home():
    return render_template('home.html', current_user=current_user)

@login_required
@appBlueprint.route("/browse")
def browse():
    communities_all = sqlDB.session.query(Community).all()
    return render_template('browse.html', communities=communities_all)

@login_required
@appBlueprint.route("/create", methods=['GET', 'POST'])
def create_community():
    community_create_form = Community_Create_Form()
    if request.method == 'POST':
        if community_create_form.validate_on_submit() and community_create_form.community_create_submit.data:
            if sqlDB.session.query(Community).filter_by(name=community_create_form.name.data).first():
                return 'error' #TODO ERROR Handling
            else:
                new_community = Community(
                    name=community_create_form.name.data,
                    dis=community_create_form.dis.data)
                sqlDB.session.add(new_community)

                new_users_communities_assocation = Users_Communities_Assocation(
                    user=current_user,
                    community= new_community,
                    role=User_Community_Enum.owner
                )
                sqlDB.session.add(new_users_communities_assocation)

                sqlDB.session.commit()
                return redirect(url_for('app.community', community_code=new_community.code))
    return render_template('create_community.html',
    community_create_form=community_create_form
    )

@login_required
@appBlueprint.route("/c/<community_code>")
def community(community_code):
    temp_community = sqlDB.session.query(Community).filter_by(code=community_code).first_or_404()
    return redirect(url_for('app.community_text_channel', community_code=community_code, channel_code=temp_community.text_channels[0].code))


@login_required
@appBlueprint.route("/c/<community_code>/t/<channel_code>")
def community_text_channel(community_code, channel_code):
    temp_community = sqlDB.session.query(Community).filter_by(code=community_code).first_or_404()
    temp_channel = temp_community.text_channels.first_or_404()

    return render_template('/textchannel.html',
        current_user=current_user,
        community=temp_community,
        channel=temp_channel
    )
 

@appBlueprint.route("/")
def front():
    return render_template('front.html')
