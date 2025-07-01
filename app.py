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
    res = cur.execute("SELECT * from dhtreadings")
    print(res.fetchone())
    return render_template("base.html")
