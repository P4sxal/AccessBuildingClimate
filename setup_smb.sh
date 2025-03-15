#!/bin/bash
#do not forget to make this script executable after coping
#e.g. chmod +x setup.sh

#add new user
/usr/sbin/adduser --system mydongle

#copy SHT30_Software and change userrights
/bin/mkdir -m 0777 /usr/local/mydongle
/bin/chown -R mydongle /home/pi/SHT30_software
/bin/mv /home/pi/SHT30_software/* /usr/local/mydongle/
/bin/rm -r /home/pi/SHT30_software/ /home/pi/setup.sh
/bin/echo "user created and files copied"

#ask User for sensor location
/bin/echo "What's the name of the Sensor location?"
read sensloc
echo "export SENSORLOC=$sensloc" | sudo tee -a /etc/profile.d/mydongle.sh
#/bin/echo "SENSORLOC="$SENSORLOC | sudo /bin/tee -a /etc/environment
#source /etc/environment

#set default smb drive
/bin/echo "//rose/OfficeLog        /mnt/officelog  cifs    username=rasp12,file_mode=0777\
,password=P,uid=mydongle,gid=pi,_netdev,x-systemd.automount,nofail" | sudo tee -a /etc/fstab
/bin/echo "export DONGLELOGDEST=/mnt/officelog" | sudo tee -a /etc/profile.d/mydongle.sh
/bin/mount -a
/bin/echo "environment variables created, logDest mounted"

#copy service and timer file
/bin/cp /usr/local/mydongle/mydongle.service /etc/systemd/system
/bin/cp /usr/local/mydongle/mydongle.timer /etc/systemd/system

/usr/sbin/usermod -a -G gpio,i2c mydongle
/bin/systemctl daemon-reload
/bin/systemctl enable mydongle.timer
/bin/systemctl start mydongle.timer

/bin/echo "AccessBuildingClimate Dongle activated"