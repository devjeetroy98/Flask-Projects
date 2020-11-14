from flask import Blueprint
from flask.helpers import flash
from flask_login.utils import login_user
from flask import render_template, redirect, url_for, request
from main.users.forms import RegistrationForm, LoginForm, Reset_req_form,Reset_password_form
from main import bcrypt, db
from main.models import User
from flask_login import current_user, logout_user, login_required
from main.users.utils import send_mail

users = Blueprint('users',__name__)

@users.route('/register', methods=["GET", "POST"])
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
            return redirect(url_for('users.login_page'))
        else:
            return render_template("register.html",form=form)


@users.route('/login', methods=["GET", "POST"])
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
                return redirect(url_for('users.dashboard_page'))
            else:
                flash('Entered credentials doesn\'t match!','danger')
                return redirect(url_for('users.login_page'))
        else:
            flash('Please fill the required fields!','danger')
            return render_template("login.html",form=form)

@users.route('/dashboard')
@login_required
def dashboard_page():
    if current_user.is_authenticated:
        return render_template("dashboard.html", data=current_user)
    else:
        return "<h2>Authentication Failed!</h2>"


@users.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Successfully Logged Out!','success')
        return redirect(url_for('users.login_page'))
    else:
        return "<h2>Authentication Failed!</h2>"

@users.route("/reset-password", methods=["GET","POST"])
def reset_req():
    form = Reset_req_form()
    if current_user.is_authenticated:
        return redirect(url_for('others.home_page'))
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        send_mail(user)
        flash("An email with reset link has been sent.","info")
        return redirect(url_for('users.login_page'))
    return render_template('reset_req.html', form=form)


@users.route("/reset-password/<token>", methods=["GET","POST"])
def reset_done(token):
    form = Reset_password_form()
    if current_user.is_authenticated:
        return redirect(url_for('others.home_page'))
    user= User.verify_reset_token(token)
    if user is None:
        flash('The token is either invalid or expired!','warning')
        return redirect(url_for('users.reset_req'))
    else:
        if form.validate_on_submit():
            hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hash_pass
            db.session.commit()
            flash('Password Updated Successfully!','success')
            return redirect(url_for('users.login_page'))
    return render_template('reset_password.html', form=form)