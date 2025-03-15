#!/bin/bash
source /etc/profile.d/mydongle.sh
#destination="$DONGLELOGDEST"
sensorloc="$SENSORLOC"
#/usr/bin/python3 logClima.py.py -dst "$destination" -loc "$sensorloc"
/usr/bin/python3 logClima.py -loc "$sensorloc"
