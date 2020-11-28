from wtforms import StringField, BooleanField, SubmitField, TextAreaField, PasswordField, SelectField,  DecimalField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileRequired

class Community_Create_Form(FlaskForm):
    """Form to create new community"""
    name = StringField('Name', [InputRequired()])
    dis = TextAreaField('Description', [InputRequired()])
    community_create_submit = SubmitField('Create')

class Login_Form(FlaskForm):
    """Form to create new community"""
    email = EmailField('Email', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    login_submit = SubmitField('Login')

class Signup_Form(FlaskForm):
    """Form to create new user"""
    name = StringField('Name', [InputRequired()])
    email = EmailField('Email', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    password_confirm = PasswordField('Password', [InputRequired()])
    signup_submit = SubmitField('Signup')

class User_Settings_Form(FlaskForm):
    """Form to create new user"""
    name = StringField('Name', [InputRequired()])
    profile_avatar = FileField()
    user_settings_submit = SubmitField('Save')
