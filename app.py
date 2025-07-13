import sqlite3
from flask import Flask, g, render_template, request
from datetime import datetime

app = Flask(__name__)

DATABASE = "./sensordata.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def web_app():
    cur = get_db().cursor()

    raw_date = request.args.get("date")
    if raw_date:
        try:
            parse_date = datetime.strptime(raw_date, "%Y-%m-%d")
            formatted_date = datetime.strftime(parse_date, "%m/%d/%y")
        except ValueError:
            formatted_date = None

    if raw_date:
        search_query = """
            SELECT currentdate, temperature, humidity
            FROM dhtreadings
            WHERE currentdate = ?
            ORDER BY id
            DESC
        """
        history = cur.execute(search_query,(formatted_date,)).fetchall()
    else:
        all_query = """
            SELECT currentdate, temperature, humidity
            FROM dhtreadings
            ORDER BY id
            DESC
        """
        history = cur.execute(all_query).fetchall()


    if history is None:
        history = {"currentdata": "N/A", "temperature": "N/A", "humidity": "N/A"}

    latest_query = """
        SELECT temperature, humidity
        FROM dhtreadings
        ORDER BY id
        DESC
        LIMIT 1
    """

    latest = cur.execute(latest_query).fetchone()

    if latest is None:
        latest = {"temperature": "N/A", "humidity": "N/A"}

    return render_template("index.html", history=history, latest=latest)
