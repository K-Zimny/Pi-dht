import board
from adafruit_bme280 import basic as adafruit_bme280
import sqlite3
from datetime import datetime

i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
DATABASE = "sensordata.db"

def handle_temp():
    temp = round((bme280.temperature * (9/5)) + 32, 1)
    print("Temperature: " + str(temp) + " F")
    
    return temp


def handle_hum():
    hum = round(bme280.humidity, 1) 
    print("Humidity: " + str(hum) + " %")

    return hum


def handle_db():
    temp = handle_temp()
    hum = handle_hum()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = (temp, hum, timestamp, 'DHT Office')

    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO dhtreadings_test(temperature, humidity, timestamp, device) Values(?,?,?,?)", data)   
    con.commit()
    print("Written to disk")

    con.close()


handle_db()

exit()
