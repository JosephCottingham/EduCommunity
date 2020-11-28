from flask_login import UserMixin
from flask_login import current_user
from sqlalchemy.orm import relationship, subqueryload, lazyload
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, timedelta
import uuid, random, copy
from enum import Enum
from edu_community import login_manager, sqlDB, mongoDB, app
import urllib
from werkzeug.utils import secure_filename

@login_manager.user_loader
def load_user(user_id):
    return sqlDB.session.query(User).get(user_id)

class User_Community_Enum(Enum):
    member = 0
    mode = 1
    owner = 2

 

communities_community_tags = sqlDB.Table("communities_community_tags", 
    sqlDB.Column("community_id", sqlDB.Integer, sqlDB.ForeignKey("communities.id")), 
    sqlDB.Column("community_tag_id", sqlDB.Integer, sqlDB.ForeignKey("community_tags.id")),
)

class Users_Communities_Assocation(sqlDB.Model):
    __tablename__ = 'users_communities_assocations'
    user_id = sqlDB.Column(sqlDB.Integer, sqlDB.ForeignKey("users.id"), primary_key=True)
    community_id = sqlDB.Column(sqlDB.Integer, sqlDB.ForeignKey("communities.id"), primary_key=True)
    role = sqlDB.Column(sqlDB.Enum(User_Community_Enum), index=False, nullable=False, default=User_Community_Enum.member)
    user = sqlDB.relationship('User', back_populates='communities')
    community = sqlDB.relationship('Community', back_populates='users')

    def __init__(self, user, community, role=User_Community_Enum.member):
        """
        docstring
        """
        self.user = user
        self.community = community
        self.role = role


class User(sqlDB.Model, UserMixin):

    __tablename__ = 'users'

    id = sqlDB.Column(sqlDB.Integer, primary_key = True, autoincrement=True)
    code = sqlDB.Column(sqlDB.String(36), primary_key=False, autoincrement=False, unique=True, nullable=False)

    created_datetime = sqlDB.Column(sqlDB.DateTime(), default=datetime.now())
    modified_datetime = sqlDB.Column(sqlDB.DateTime(), onupdate=datetime.utcnow())

    active = sqlDB.Column(sqlDB.Boolean(), index=True, default=True)

    email = sqlDB.Column(sqlDB.String(64), index=True, unique=True)
    name = sqlDB.Column(sqlDB.String(64), index=True, unique=False)

    password_hash = sqlDB.Column(sqlDB.String(128), index=True)
    password_clear = sqlDB.Column(sqlDB.String(128), index=True)

    communities = sqlDB.relationship('Users_Communities_Assocation', back_populates='user')

    def __init__(self, email, password, name):
        code = 'US__' + uuid.uuid4().hex
        while (sqlDB.session.query(User).filter_by(code=code).first() != None):
            code = 'US__' + uuid.uuid4().hex
        self.code = code   
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.password_clear = password
        filename = secure_filename(self.code + ".jpg")
        path = os.path.join(app.static_folder, 'img', 'user_avatars', filename)
        urllib.urlretrieve(('https://picsum.photos/200?random'), (path))
    def check_password(self, password):
        return check_password_hash(self.password_hash,password)


class Community(sqlDB.Model):

    __tablename__ = 'communities'

    id = sqlDB.Column(sqlDB.Integer, primary_key = True, autoincrement=True)
    code = sqlDB.Column(sqlDB.String(36), primary_key=False, autoincrement=False, unique=True, nullable=False)

    created_datetime = sqlDB.Column(sqlDB.DateTime(), default=datetime.now())
    modified_datetime = sqlDB.Column(sqlDB.DateTime(), onupdate=datetime.utcnow())

    active = sqlDB.Column(sqlDB.Boolean(), index=True, default=True)

    name = sqlDB.Column(sqlDB.String(64), index=True, unique=False)
    dis = sqlDB.Column(sqlDB.Text(), index=True, unique=False)

    users = sqlDB.relationship('Users_Communities_Assocation', back_populates='community')

    community_tags = sqlDB.relationship("Community_Tag", back_populates="communities", secondary=communities_community_tags)

    text_channels = sqlDB.relationship('Text_Channel', back_populates='community', lazy='dynamic')

    members_online = sqlDB.Column(sqlDB.Integer, index=True, unique=False, default=0)

    def __init__(self, name, dis):
        code = 'CO__' + uuid.uuid4().hex
        while (sqlDB.session.query(User).filter_by(code=code).first() != None):
            code = 'CO__' + uuid.uuid4().hex
        self.code = code   
        self.name = name
        self.dis = dis
        new_text_channel = Text_Channel('general', 'general')
        sqlDB.session.add(new_text_channel)
        self.text_channels.append(new_text_channel)
        sqlDB.session.commit()

class Text_Channel(sqlDB.Model):

    __tablename__ = 'text_channels'

    id = sqlDB.Column(sqlDB.Integer, primary_key = True, autoincrement=True)
    code = sqlDB.Column(sqlDB.String(36), primary_key=False, autoincrement=False, unique=True, nullable=False)

    created_datetime = sqlDB.Column(sqlDB.DateTime(), default=datetime.now())
    modified_datetime = sqlDB.Column(sqlDB.DateTime(), onupdate=datetime.utcnow())

    active = sqlDB.Column(sqlDB.Boolean(), index=True, default=True)

    name = sqlDB.Column(sqlDB.String(64), index=True, unique=False)
    dis = sqlDB.Column(sqlDB.Text(), index=True, unique=False)

    community_id = sqlDB.Column(sqlDB.Integer, sqlDB.ForeignKey('communities.id'))
    community = sqlDB.relationship('Community', back_populates='text_channels')

    mongodb_chat_history_id = sqlDB.Column(sqlDB.String(64), index=False, unique=True)

    def __init__(self, name, dis):
        code = 'TC__' + uuid.uuid4().hex
        while (sqlDB.session.query(User).filter_by(code=code).first() != None):
            code = 'TC__' + uuid.uuid4().hex
        self.code = code   
        self.name = name
        self.dis = dis
        new_document = mongoDB.channel_messages.insert_one({msgs : []})
        self.mongodb_chat_history_id = str(new_document.inserted_id)

class Community_Tag(sqlDB.Model):

    __tablename__ = 'community_tags'

    id = sqlDB.Column(sqlDB.Integer, primary_key = True, autoincrement=True)
    code = sqlDB.Column(sqlDB.String(36), primary_key=False, autoincrement=False, unique=True, nullable=False)

    created_datetime = sqlDB.Column(sqlDB.DateTime(), default=datetime.now())
    modified_datetime = sqlDB.Column(sqlDB.DateTime(), onupdate=datetime.utcnow())

    active = sqlDB.Column(sqlDB.Boolean(), index=True, default=True)

    name = sqlDB.Column(sqlDB.String(64), index=True, unique=False)

    communities = sqlDB.relationship("Community", back_populates="community_tags", secondary=communities_community_tags)

    def __init__(self, name):
        code = 'CT__' + uuid.uuid4().hex
        while (sqlDB.session.query(User).filter_by(code=code).first() != None):
            code = 'CT__' + uuid.uuid4().hex
        self.code = code   
        self.name = name
