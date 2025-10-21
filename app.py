# app.py
import sqlite3
from flask import Flask, g, render_template, request
from datetime import datetime

app = Flask(__name__)

DATABASE = "./sensordata.db"

LATEST_QUERY = """
    SELECT temperature, humidity, timestamp
    FROM bme_readings
    ORDER BY id DESC
    LIMIT 1
"""

ALL_QUERY = """
    SELECT timestamp, temperature, humidity
    FROM bme_readings
    ORDER BY id DESC
"""

# Filter by calendar day using SQLite's date() on ISO timestamp
SEARCH_QUERY = """
    SELECT timestamp, temperature, humidity
    FROM bme_readings
    WHERE date(timestamp) = ?
    ORDER BY id DESC
"""

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/")
def web_app():
    cur = get_db().cursor()

    # === Query ===
    # Check if a date was submitted and use that for the search, else return all entries. 
    raw_date = request.args.get("date")
    valid_date = None

    if raw_date:
        try:
            # Expecting YYYY-MM-DD from <input type="date">
            datetime.strptime(raw_date, "%Y-%m-%d")
            valid_date = raw_date
        except ValueError:
            valid_date = None  # fall back to all

    if valid_date:
        history = cur.execute(SEARCH_QUERY, (valid_date,)).fetchall()  # search by date
    else:
        history = cur.execute(ALL_QUERY).fetchall() # show all
    # === end Query ===

    # === Latest Reading ===
    latest = cur.execute(LATEST_QUERY).fetchone()
    if latest is None:
        latest = {"temperature": "N/A", "humidity": "N/A", "timestamp": "N/A"}
    # === end Latest Reading ===

    # === Chart Data ===
    history_for_chart = list(reversed(history))

    chart_labels = [row["timestamp"] for row in history_for_chart]      # ISO strings → Plotly time axis
    chart_temperature = [row["temperature"] for row in history_for_chart]
    chart_humidity = [row["humidity"] for row in history_for_chart]
    # === end Chart Data ===

    return render_template(
        "index.html",
        history=history,  # rows include timestamp/temperature/humidity
        latest=latest,
        chart_labels=chart_labels,
        chart_temperature=chart_temperature,
        chart_humidity=chart_humidity,
    )

if __name__ == "__main__":
    app.run(debug=True)
