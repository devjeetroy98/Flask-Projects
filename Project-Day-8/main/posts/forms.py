from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from main.models import User
from wtforms.validators import ValidationError


class PostForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired()])
    content= TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post!")


def validate_username(self, username):
    user = User.query.filter_by(username=username).first()
    if user:
        raise ValidationError('User already exist!')