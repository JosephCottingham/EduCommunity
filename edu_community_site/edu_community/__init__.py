import os, json, logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
from flask_socketio import SocketIO


app = Flask(__name__, template_folder="../frontend", static_folder="../frontend/assets")

app.config['SECRET_KEY'] = "secrete"

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

#################################
### DATABASE SETUPS ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///siteData.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

sqlDB = SQLAlchemy(app)


###########################
#### LOGIN CONFIGS #######
#########################


login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "user.login"

###########################
#### DATABASE CREATE #####
#########################

from .sql_models import Community, Community_Tag, User
sqlDB.create_all()
sqlDB.session.commit()
# u = User(email='temp@temp.org', password='temp', role="super_admin", name='Temp')
# db.session.add(u)
# db.session.commit()

###########################
#### BLUEPRINT CONFIGS ####
#########################
from edu_community.views import appBlueprint
app.register_blueprint(appBlueprint)

###########################
#### ADMIN CONFIGS #######
#########################
from flask_admin import Admin
admin = Admin(app)
from flask_admin.contrib.sqla import ModelView
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Ballot, db.session))
# admin.add_view(ModelView(Event, db.session))
# # admin.add_view(ModelView(Judge, db.session))
# admin.add_view(ModelView(Outstanding, db.session))
# admin.add_view(ModelView(Competitor_Part, db.session))
# admin.add_view(ModelView(School, db.session))
# admin.add_view(ModelView(Team, db.session))




app.app_context().push()
