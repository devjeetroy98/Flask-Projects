from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL


class MyForm(FlaskForm):
    url = StringField("URL", validators=[DataRequired(), Length(min= 10, max= 400), URL()])
    keyword =  StringField("Keyword", validators=[DataRequired(), Length(min= 5, max= 30)])
    submit = SubmitField("Submit")