from main import mail
from flask import url_for
from flask_mail import Message


def send_mail(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Requested', sender="noreply@demo.com", recipients=[user.email])
    msg.body = f'''
To reset your password, kindly visit the link:
{url_for('users.reset_done',token = token, _external = True)}
Kindly ignore if this request is not done by you!
    '''
    mail.send(msg)




