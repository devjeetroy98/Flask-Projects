from flask import Blueprint
from flask import render_template
others = Blueprint('others',__name__)

@others.route('/')
@others.route('/homepage')
def home_page():
    return render_template('homepage.html')