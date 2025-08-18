import board
import adafruit_dht
import sqlite3
from datetime import datetime

dht_device = adafruit_dht.DHT22(board.D17)

def handle_temp():
    temp = round((dht_device.temperature * (9/5)) + 32, 1)
    print("Temperature: " + str(temp) + " F")
    
    return temp


def handle_hum():
    hum = round(dht_device.humidity, 1) 
    print("Humidity: " + str(hum) + " %")

    return hum


def handle_db():
    temp = handle_temp()
    hum = handle_hum()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = (temp, hum, timestamp, 'DHT Office')

    con = sqlite3.connect("sensordata.db")
    cur = con.cursor()
    cur.execute("INSERT INTO dhtreadings_test(temperature, humidity, timestamp, device) Values(?,?,?,?)", data)   
    con.commit()
    print("Written to disk")

    con.close()


handle_db()

exit()
