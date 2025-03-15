#!/bin/python3
from dongleSHT30 import SHT30_dongle
import mariadb

conn = mariadb.connect(host="192.168.178.36", user="pi", password="RaspBerryPi1!",database="mybase")
cur = conn.cursor()  

dongle = SHT30_dongle()
clim= dongle.log_clima_dict()
#print(clim)
query = f"insert myclim (time, temperature, humidity, timestamp, location, hostname)\
      values ('{clim['time']}',{clim['temperature']},{clim['humidity']},\
        {clim['timestamp']},'{clim['location']}','{clim['hostname']}')"
cur.execute(query)
conn.commit()