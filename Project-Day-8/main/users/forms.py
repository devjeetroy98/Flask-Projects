from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
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
        else:
            return True
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail already registered!')

class LoginForm(FlaskForm):
    # username= StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email= StringField('E-Mail', validators=[DataRequired(), Email()])
    password= PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In!")


class  Reset_req_form(FlaskForm):
    email= StringField('E-Mail', validators=[DataRequired(), Email()])
    submit = SubmitField("Get Reset Link")

    def validate_email_reset(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user in None:
            raise ValidationError('This email is not registerd! Please register your email id!')

class  Reset_password_form(FlaskForm):
    password= PasswordField("Password", validators=[DataRequired(), Length(min=5, max=20)])
    confirm_password= PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Submit Password")