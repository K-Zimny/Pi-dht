import board
import sqlite3
from datetime import datetime
from adafruit_bme280 import basic as adafruit_bme280

# === Sensor Configuration ===
i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# === Database Configuration ===
DATABASE = "/home/kz/bme/sensordata.db"

# === Sensor Reading Functions ===
def get_temperature():
    """Read temperature from BME280 sensor and convert to Fahrenheit."""
    temp = round((bme280.temperature * (9/5)) + 32, 1)
    print(f"Temperature: {temp} F")
    return temp

def get_humidity():
    """Read humidity from BME280 sensor."""
    hum = round(bme280.humidity, 1)
    print(f"Humidity: {hum} %")
    return hum

# === Database Functions ===
def save_reading(temp, hum, timestamp):
    """Save sensor reading to database."""
    data = (temp, hum, timestamp, 'BME Crawlspace')
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO bme_readings(temperature, humidity, timestamp, device) VALUES(?,?,?,?)",
        data
    )
    connection.commit()
    print("Written to disk")
    connection.close()

# === Main Execution ===
def main():
    """Main function to read sensor data and save to database."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temp = get_temperature()
    hum = get_humidity()
    
    save_reading(temp, hum, timestamp)

if __name__ == "__main__":
    main()
