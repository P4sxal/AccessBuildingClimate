This repo contains everything to build a system for monitoring temperature and humidity in a building.
Dedicated sensors are built to measure and send the data via Http API to a host server.
The collected data is stored and visualized with a web interface.

## Sensor design

The Sensor is based on the SHT30 IC from Sensiron, a digital temperature and humidity sensor.
https://sensirion.com/products/catalog/SHT30-DIS-B

A custom PCB was designed to read the sensor from a raspberry zero w.

SHT30 dongle:

<img alt="SHT30Dongle" src="SHT30_sensor/SHT_Dongle_1.jpeg" width="300">
<img width="300" alt="CAD view" src="https://github.com/user-attachments/assets/b2f2543c-d58d-43da-8d38-84cb9449bdcb" />
<img width="300" alt="eCAD view" src="https://github.com/user-attachments/assets/61205fe3-e6fc-4e41-be58-4a5ceeb42998" />




## Sensor Software

The sensor is read via the I2C bus using a python script.


## Server API

to be written down.
