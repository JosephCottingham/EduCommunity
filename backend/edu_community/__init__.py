import os, json, logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import datetime
from ballotSite.config import Config
from flask_mail import Mail
import stripe

path = os.path.join(os.getcwd(), os.path.join('configs', 'testConfig.json'))

with open(os.path.join(os.getcwd(), 'AppSettings.Config')) as config_file:
    app_config = json.load(config_file)
    config = Config.get_instance(Config.MODES.get(app_config.get('MODE')))

app = Flask(__name__)

app.config['STRIPE_SECRET_KEY'] = config.STRIPE_SECRET_KEY
app.config['SECRET_KEY'] = config.SECRET_KEY

stripe.api_key = app.config['STRIPE_SECRET_KEY']


gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


##################################
### MAIL SETUPS #################
################################

app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
mail = Mail(app)


#################################
### UPLOAD SYSTEM ##############
###############################


app.config['UPLOADED_JUDGECSV_DEST'] = config.UPLOADED_FILES_DEST


#################################
### DATABASE SETUPS ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app, db)


###########################
#### LOGIN CONFIGS #######
#########################


login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "judge.login"

###########################
#### DATABASE CREATE #####
#########################

from .models import User, Ballot, SuperAdminModelView, Competitor_Part, Team, Event, Judge, School, Ballot, Event_Purchase_Code, Outstanding
db.create_all()
db.session.commit()
# u = User(email='temp@temp.org', password='temp', role="super_admin", name='Temp')
# db.session.add(u)
# db.session.commit()

###########################
#### BLUEPRINT CONFIGS ####
#########################
from ballotSite.views import appBlueprint


app.register_blueprint(appBlueprint)

###########################
#### ADMIN CONFIGS #######
#########################
from flask_admin import Admin
admin = Admin(app)
from .models import SuperAdminModelView
admin.add_view(SuperAdminModelView(User, db.session))
admin.add_view(SuperAdminModelView(Ballot, db.session))
admin.add_view(SuperAdminModelView(Event, db.session))
# admin.add_view(SuperAdminModelView(Judge, db.session))
admin.add_view(SuperAdminModelView(Outstanding, db.session))
admin.add_view(SuperAdminModelView(Competitor_Part, db.session))
admin.add_view(SuperAdminModelView(School, db.session))
admin.add_view(SuperAdminModelView(Team, db.session))




app.app_context().push()
