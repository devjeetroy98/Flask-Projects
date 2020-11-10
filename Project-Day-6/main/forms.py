from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import User
from wtforms.validators import ValidationError

class RegistrationForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email= StringField('E-Mail', validators=[DataRequired(), Email()])
    password= PasswordField("Password", validators=[DataRequired(), Length(min=5, max=20)])
    confirm_password= PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up!")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User already exist!')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail already registered!')

class LoginForm(FlaskForm):
    # username= StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email= StringField('E-Mail', validators=[DataRequired(), Email()])
    password= PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In!")

class PostForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired()])
    content= TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post!")


def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError('User already exist!')