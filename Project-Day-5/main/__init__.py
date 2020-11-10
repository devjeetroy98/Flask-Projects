from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY']='2dc16a17401388067c61dafa40a5c72e2836844b0b9efbb367a7'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///auth.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from main import routes