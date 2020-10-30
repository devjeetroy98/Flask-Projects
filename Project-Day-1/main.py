from flask import Flask, render_template, url_for, request
from forms import UserForm

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY']= '0f0a9fc9719b259462005c65712e423e0195c699786aed5ecd87'
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

        return render_template('dashboard.html', data = [name,email,age])

if __name__ == "__main__":
    app.run(debug=True)