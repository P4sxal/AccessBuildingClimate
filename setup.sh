#!/bin/sh
#do not forget to make this script executable after coping
#e.g. chmod +x setup.sh

#add new user
/usr/sbin/adduser --system mydongle

#copy SHT30_Software and change userrights
/bin/mv /home/pi/SHT30_software/* /home/mydongle/
/bin/chown -R mydongle /home/pi/SHT30_software

/bin/echo "user created and files copied"

#copy service and timer file
/bin/cp /home/mydongle/mydongle.service /etc/systemd/system
/bin/cp /home/mydongle/mydongle.timer /etc/systemd/system

/usr/sbin/usermod -a -G gpio,i2c mydongle
/bin/systemctl daemon-reload
/bin/systemctl enable mydongle.timer
/bin/systemctl start mydongle.timer

/bin/echo "AccessBuildingClimate Dongle activated"