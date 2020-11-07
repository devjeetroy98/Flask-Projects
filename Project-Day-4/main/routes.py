from flask.helpers import flash
from flask_login.utils import login_user
from main import app
from flask import render_template, redirect, url_for, request
from main.forms import RegistrationForm, LoginForm
from main import bcrypt, db
from main.models import User
from flask_login import current_user, logout_user, login_required

@app.route('/')
@app.route('/homepage')
def home_page():
    return render_template('homepage.html')

@app.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template("register.html",form=form)
    else:
        if form.validate_on_submit():
            hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hash_pass)
            db.session.add(user)
            db.session.commit()
            flash('Account Created Successfully!','success')
            return redirect(url_for('login_page'))
        else:
            return render_template("register.html",form=form)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if request.method == 'GET':
        return render_template("login.html",form=form)
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=False)
                flash('Successfully logged in!','success')
                return redirect(url_for('dashboard_page'))
            else:
                flash('Entered credentials doesn\'t match!','danger')
                return redirect(url_for('login_page'))
        else:
            flash('Please fill the required fields!','danger')
            return render_template("login.html",form=form)

@app.route('/dashboard')
@login_required
def dashboard_page():
    if current_user.is_authenticated:
        return render_template("dashboard.html", data=current_user)
    else:
        return "<h2>Authentication Failed!</h2>"


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login_page'))
    else:
        return "<h2>Authentication Failed!</h2>"