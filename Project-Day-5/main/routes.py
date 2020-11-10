from flask.helpers import flash
from flask_login.utils import login_user
from main import app
from flask import render_template, redirect, url_for, request
from main.forms import RegistrationForm, LoginForm, PostForm, validate_username
from main import bcrypt, db
from main.models import User,Posts
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
        if form.validate_on_submit() and form.validate_username(form.username.data):
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
        flash('Successfully Logged Out!','success')
        return redirect(url_for('login_page'))
    else:
        return "<h2>Authentication Failed!</h2>"

@app.route("/posts")
@login_required
def readblog():
    if current_user.is_authenticated:
        posts = Posts.query.all()
        return render_template("readblog.html",posts=posts)
    else:
        return "<h2>Not Authorized!</h2>"

@app.route("/post/new", methods=["GET","POST"])
@login_required
def writeblog():
    form=PostForm()
    if request.method == "GET":
        if current_user.is_authenticated:
            return render_template("postcontent.html", form=form)
        else:
            return "<h2>Not Authorized!</h2>"
    else:
        if form.validate_on_submit():
            post = Posts(title=form.title.data, content=form.content.data, author=current_user.username)
            db.session.add(post)
            db.session.commit()
            flash('Posted Successfully!','success')
            return redirect(url_for('readblog'))
        else:
            return render_template("postcontent.html", form=form)

@app.route("/posts/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_blog(post_id):
    if request.method == "POST":
        if current_user.is_authenticated:
            post = Posts.query.filter_by(post_id=post_id).first()
            if post.author == current_user.username:
                db.session.delete(post)
                db.session.commit()
                flash('Post deleted!','success')
                return redirect(url_for('readblog'))
        else:
            return "<h2>Not Authorized!</h2>"

@app.route("/posts/update/<int:post_id>", methods=["GET","POST"])
@login_required
def update_blog(post_id):
    form=PostForm()
    if request.method == "POST":
        if current_user.is_authenticated:
            post = Posts.query.filter_by(post_id=post_id).first()
            if form.validate_on_submit():
                post.title = form.title.data
                post.content = form.content.data
                db.session.commit()
                flash('Updated Successfully!','success')
                return redirect(url_for('readblog'))
            form.title.data = post.title
            form.content.data = post.content
            return render_template("postcontent.html", form=form)
        else:
            return "<h2>Not Authorized!</h2>"