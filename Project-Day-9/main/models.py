from main import db,login_manager
from flask import current_app
from flask_login import UserMixin
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

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