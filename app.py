import sqlite3
from datetime import datetime
from flask import Flask, g, render_template, request

# === Flask App Initialization ===
app = Flask(__name__)

# === Database Configuration ===
DATABASE = "./sensordata.db"

# === SQL Queries ===
LATEST_QUERY = """
    SELECT timestamp,temperature, humidity
    FROM bme_readings
    ORDER BY id DESC
    LIMIT 1
"""

ALL_QUERY = """
    SELECT timestamp, temperature, humidity
    FROM bme_readings
    ORDER BY id DESC
"""

SEARCH_QUERY = """
    SELECT timestamp, temperature, humidity
    FROM bme_readings
    WHERE date(timestamp) = ?
    ORDER BY id DESC
"""

# === Database Connection Management ===
def get_db():
    """Get or create database connection for the current request."""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close database connection at the end of each request."""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# === Routes ===
@app.route("/")
def web_app():
    """Main route: Display sensor readings with optional date filtering."""
    cursor = get_db().cursor()

    # Process date filter from query parameters
    raw_date = request.args.get("date")
    valid_date = None

    if raw_date:
        try:
            # Validate YYYY-MM-DD format from <input type="date">
            datetime.strptime(raw_date, "%Y-%m-%d")
            valid_date = raw_date
        except ValueError:
            valid_date = None  # Fall back to showing all records

    # Fetch history data
    if valid_date:
        history = cursor.execute(SEARCH_QUERY, (valid_date,)).fetchall()
    else:
        history = cursor.execute(ALL_QUERY).fetchall()

    # Fetch latest reading
    latest = cursor.execute(LATEST_QUERY).fetchone()
    if latest is None:
        latest = {"temperature": "N/A", "humidity": "N/A", "timestamp": "N/A"}

    # Prepare chart data (reverse for chronological order)
    history_for_chart = list(reversed(history))
    chart_labels = [row["timestamp"] for row in history_for_chart]
    chart_temperature = [row["temperature"] for row in history_for_chart]
    chart_humidity = [row["humidity"] for row in history_for_chart]

    return render_template(
        "index.html",
        history=history,
        latest=latest,
        chart_labels=chart_labels,
        chart_temperature=chart_temperature,
        chart_humidity=chart_humidity,
    )

if __name__ == "__main__":
    app.run(debug=True)
