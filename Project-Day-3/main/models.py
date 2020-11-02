from flask_sqlalchemy import SQLAlchemy
from main import db

class User(db.Model):
    username = db.Column(db.String(20), primary_key = True)
    email = db.Column(db.String(100), nullable= False, unique=True)
    age = db.Column(db.Integer, nullable= False, default=0)

    def __init__(self,username,email,age):
        self.username = username
        self.email=email
        self.age=age
        
    def __repr__(self) -> str:
        return f"User('{self.username}','{self.email}','{self.age}')"