import sqlite3
from flask import Flask
from flask import g
from flask import render_template

app = Flask(__name__)

DATABASE = "./sensordata.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def web_app():
    cur = get_db().cursor()

    history = cur.execute("SELECT currentdate, temperature, humidity FROM dhtreadings").fetchall()
    latest = cur.execute("SELECT temperature, humidity FROM dhtreadings ORDER BY id DESC LIMIT 1").fetchone()

    return render_template("base.html", history=history, latest=latest)
