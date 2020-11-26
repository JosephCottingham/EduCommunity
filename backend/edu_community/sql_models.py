from flask_login import UserMixin
from flask_login import current_user
from sqlalchemy.orm import relationship, subqueryload, lazyload
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, timedelta
import uuid, random, copy

@login_manager.user_loader
def load_user(user_code):
    return db.session.query(User).filter_by(code=user_code).first()


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    code = db.Column(db.String(36), primary_key=False, autoincrement=False, unique=True, nullable=False)

    created_datetime = db.Column(db.DateTime(), default=datetime.now())
    modified_datetime = db.Column(db.DateTime(), onupdate=datetime.utcnow())

    active = db.Column(db.Boolean(), index=True, default=True)

    email = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=False)

    password_hash = db.Column(db.String(128), index=True)
    password_clear = db.Column(db.String(128), index=True)


    def __init__(self, email, password, name):
        code = 'US__' + uuid.uuid4().hex
        while (db.session.query(User).filter_by(code=code).first() != None):
            code = 'US__' + uuid.uuid4().hex
        self.code = code   
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.password_clear = password

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)
    
class Community(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    code = db.Column(db.String(36), primary_key=False, autoincrement=False, unique=True, nullable=False)

    created_datetime = db.Column(db.DateTime(), default=datetime.now())
    modified_datetime = db.Column(db.DateTime(), onupdate=datetime.utcnow())

    active = db.Column(db.Boolean(), index=True, default=True)

    