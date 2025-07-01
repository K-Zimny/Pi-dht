from flask import Flask
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def web_app():
    return render_template("base.html")
