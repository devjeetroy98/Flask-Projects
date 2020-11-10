from main import db,login_manager
from flask_login import UserMixin
from flask_login import current_user
from datetime import datetime,date

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True, nullable=False)
    email = db.Column(db.String(30), unique = True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, username,email,password):
        self.username = username
        self.email = email
        self.password = password

    def __repl__(self):
        return f"User( '{self.id}' ,'{self.username}', '{self.email}' )"

class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text(),nullable=False)
    author = db.Column(db.String(20),nullable=False)
    time = db.Column(db.DateTime(),default=date.today(), onupdate=date.today())

    def __init__(self, title,content,author):
        self.title=title
        self.content=content
        self.author = author

    def __repl__(self):
        return f"Posts( '{self.title}' ,'{self.content}', '{self.time}' )"