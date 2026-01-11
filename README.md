# Raspberry Pi Temperature & Humidity Tracker

This project monitors temperature and humidity in a crawlspace using a Raspberry Pi and a BME280 sensor. It is designed for continuous environmental tracking with simple setup and reliable readings.

## Overview

The Raspberry Pi reads temperature and humidity data from a BME280 sensor and displays the values for monitoring crawlspace conditions. This helps identify moisture issues, temperature fluctuations, and long-term trends that could impact structural integrity or air quality.

## Hardware

- Raspberry Pi
- BME280 temperature, humidity, and pressure sensor
- Jumper wires
- Power supply
- Enclosure suitable for crawlspace deployment

## Features

- Real-time temperature readings  
- Real-time humidity readings  
- I2C-based sensor communication  
- Lightweight and low-power operation  
- Suitable for long-term unattended monitoring  

## Use Case

Built for crawlspaces, basements, or other enclosed areas where tracking temperature and humidity is important for mold prevention, moisture control, and general environmental awareness.

## Setup Notes

- Enable I2C on the Raspberry Pi.
- Ensure the BME280 is wired correctly to the Pi’s I2C pins.
- Place the sensor where airflow is representative of the crawlspace.
- Protect the sensor from direct water exposure or condensation.
