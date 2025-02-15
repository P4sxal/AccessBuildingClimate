#!/bin/sh

#add new user
adduser --system mydongle

#copy SHT30_Software and change userrights
chown -R mydongle /home/pi/SHT30_software
mv /home/pi/SHT30_software/ /home/mydongle/

echo "ok, lets continue"

#copy service and timer file
cp /home/mydongle/mydongle.service /etc/systemd/system
cp /home/mydongle/mydongle.timer /etc/systemd/system

usermod -a -G gpio,i2c mydongle
systemctl daemon-reload
systemctl enable mydongle.timer
systemctl start mydongle.timer