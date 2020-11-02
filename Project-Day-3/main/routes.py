from flask.helpers import url_for
from main import app,db
from flask import Flask, render_template, request, redirect
from main.forms import UserForm
from main.models import User

@app.route('/')
def home_page():
    return render_template('homepage.html')

@app.route("/about")
def about_page():
    return render_template('about.html')

@app.route("/form", methods=['GET', 'POST'])
def form_page():
    if request.method == 'GET':
        form = UserForm()
        return render_template('form.html', form=form)
    else:
        name = request.form['username']
        email = request.form['email']
        age = request.form['age']

        data = User(username=name,email=email,age=age)
        db.session.add(data)
        db.session.commit()

        datas = User.query.all()
        return render_template('dashboard.html', datas=datas)

@app.route("/dashboard", methods=['GET'])
def dashboard():
    datas = User.query.all()
    return render_template('dashboard.html', datas=datas)