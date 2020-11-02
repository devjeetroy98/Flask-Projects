from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired(), Length(min=1, max=3)] )
    submit = SubmitField("Submit")


    