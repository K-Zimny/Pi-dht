import sqlite3
from flask import Flask, g, render_template, request
from datetime import datetime

app = Flask(__name__)

DATABASE = "./sensordata.db"

LATEST_QUERY = """
    SELECT temperature, humidity
    FROM dhtreadings
    ORDER BY id
    DESC
    LIMIT 1
"""

ALL_QUERY = """
    SELECT currentdate, temperature, humidity
    FROM dhtreadings
    ORDER BY id
    DESC
"""

SEARCH_QUERY = """
    SELECT currentdate, temperature, humidity
    FROM dhtreadings
    WHERE currentdate = ?
    ORDER BY id
    DESC
"""

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
        history = cur.execute(SEARCH_QUERY,(formatted_date,)).fetchall()
    else:
        history = cur.execute(ALL_QUERY).fetchall()

    if history is None:
        history = {"currentdata": "N/A", "temperature": "N/A", "humidity": "N/A"}

    chart_labels = [
            datetime.strptime(row["currentdate"], "%m/%d/%y").strftime("%Y-%m-%d")
            for row in history
    ]
    chart_temperature = [row["temperature"] for row in history]
    chart_humidity = [row["humidity"] for row in history]

    chart_temperatures = [row["temperature"] for row in history]
    chart_humidity = [row["humidity"] for row in history]

    latest = cur.execute(LATEST_QUERY).fetchone()
    if latest is None:
        latest = {"temperature": "N/A", "humidity": "N/A"}


    return render_template("index.html",
        history=history,
        latest=latest,
        chart_labels=chart_labels,
        chart_temperature=chart_temperature,
        chart_humidity=chart_humidity
    )
