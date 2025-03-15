#!/bin/bash
#do not forget to make this script executable after coping
#e.g. chmod +x setup.sh

#get ready for the database
/usr/bin/apt install libmariadb3 libmariadb-dev
/usr/bin/pip3 install -t "/usr/lib/python3/dist-packages" mariadb
# for older raspberry zero w, use legacy library:
#/usr/bin/pip3 install -t "/usr/lib/python3/dist-packages" mariadb==1.0.11

#add new user
/usr/sbin/adduser --system mydongle

#copy SHT30_Software and change userrights
/bin/mkdir -m 0777 /usr/local/mydongle
/bin/chown -R mydongle /home/pi/SHT30_software
/bin/mv /home/pi/SHT30_software/* /usr/local/mydongle/
/bin/rm -r /home/pi/SHT30_software/ /home/pi/setup_db.sh
/bin/echo "user created and files copied"

#ask User for sensor location
/bin/echo "What's the name of the Sensor location?"
read sensloc
/bin/echo -e "#Sensor location, modify if needed \nexport SENSORLOC=$sensloc" | sudo tee -a /etc/profile.d/mydongle.sh
#/bin/echo "SENSORLOC="$SENSORLOC | sudo /bin/tee -a /etc/environment
#source /etc/environment

#enable i2c functionality
/usr/sbin/usermod -a -G gpio,i2c mydongle
/bin/raspi-config nonint do_i2c 0

#copy service and timer file
/bin/cp /usr/local/mydongle/mydongle.service /etc/systemd/system
/bin/cp /usr/local/mydongle/mydongle.timer /etc/systemd/system

/bin/systemctl daemon-reload
/bin/systemctl enable mydongle.timer
/bin/systemctl start mydongle.timer

/bin/echo "AccessBuildingClimate Dongle activated"