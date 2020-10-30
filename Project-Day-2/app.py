from flask import Flask, render_template, request, url_for
from forms import MyForm

# For URL Shortening
import urllib.request
import json
import urllib
from xml.etree import ElementTree as ET
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from json import dumps

app = Flask(__name__)

app.config['SECRET_KEY'] = '55e39be6ed08b8a20a5824875615fafb1b8b8059138969b29ff7'

@app.route('/', methods=["GET","POST"])
def show_homepage():
    form = MyForm()
    if request.method == "GET":
        return render_template('homepage.html', form = form, data = "")
    elif request.method == "POST":
        url = request.form['url']
        keyword = request.form['keyword']

        # ! CODE LOGIC
        requestURL = ""
        status = ""
        message = ""
        title = ""
        short = ""

        url = url.replace("&", "%26")

        if keyword == "":
            keyword = url.split("/")[-1]
        requestURL = "https://shortener.tarundev.com/yourls-api.php" \
            + "?signature=92d16c5db3" \
            + "&action=shorturl" \
            + "&keyword=" + keyword \
            + "&format=json" \
            + "&url=" + url

        root = urllib.request.urlopen(requestURL).read()
        json1 = json.loads(root)
        print('\n')

        try:
            status = json1['status']
            message = json1['message']
            short = json1['shorturl']
            title = json1['title']
        except:
            print(root)

        out = "STATUS:\t\t" + status + "\n" \
            + "MESSAGE:\t" + message + "\n" \
            + "TITLE:\t\t" + title + "\n" \
            + "SHORTURL:\t" + short + "\n"

        return render_template('homepage.html', form = form, data = short)

if __name__ == "__main__":
    app.run(debug=True)