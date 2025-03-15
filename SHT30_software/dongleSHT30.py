#SHT30_Dongle_LEDs

# The dongle has three built in LEDs, green, yellow and red.
# pin 14 is green, 15 is yellow and 18 is red, mapped to raspberry zero pin naming
# pull to ground to switch on the led

#gpio interface for raspberry
from gpiozero import LED
#smbus to interface the SHT30 via I2C
import smbus
from time import sleep, ctime, time
#creating a timestamp + hostname
from os import uname, environ
import json

#which dongle can be selected by args
import argparse

parser = argparse.ArgumentParser(description='''SHT30dongle interface''')
parser.add_argument("-st",dest="sensortype",default="wired",help="'wired' or 'dongle', default 'wired'")
#parser.add_argument("-dst")
parser.add_argument("-loc",default="unknown")
args=parser.parse_args()

# define the colors
class SHT30_dongle():
    """
    Represents the dedicated Dongle with SHT30 Sensor and 3 LEDs for RPi zero

    The device is compatible to standard RPi zero, thus can be soldered without wires.
    The physical data can be found in the SHT30_sensor folder.
    Included are CAE, CAD and gerber files. 
    SHT30 address, 0x45(68), per default.
    """
    def __init__(self,smbus_adress = 1):
        
        if args.sensortype == 'wired':
            __i2c_address = 0x45
        elif args.sensortype == 'dongle':
            __i2c_address = 0x44
        else:
            raise Exception("Sensortype not found")
        
        self._green = LED(14, active_high = False)
        self._yellow = LED(15, active_high = False)
        self._red = LED(18, active_high = False)
        self._bus = smbus.SMBus(smbus_adress)
        self._i2c_address = __i2c_address
        self._update_temp_hum()
            
    def log_clima(self):
        #post the clim data in json format
        self._update_temp_hum()
        temp = self._temp
        hum = self._hum
        stringtime = ctime()
        timestamp = time()
        hostname = uname()[1]
        return json.dumps({
            "time":stringtime,
            "temperature":temp,
            "humidity":hum,
            "timestamp":timestamp,
            "location":args.loc,
            "hostname":hostname
        })
    
    def log_clima_dict(self):
        #post the clim data in json format
        self._update_temp_hum()
        temp = self._temp
        hum = self._hum
        stringtime = ctime()
        timestamp = time()
        hostname = uname()[1]
        return {
            "time":stringtime,
            "temperature":temp,
            "humidity":hum,
            "timestamp":timestamp,
            "location":args.loc,
            "hostname":hostname
        }

    def _update_temp_hum(self):
        # reads the temp and hum from the SHT30 dongle
        try:
            # Send measurement command, 0x2C
            # 0x06(06) High repeatability measurement
            self._bus.write_i2c_block_data(self._i2c_address, 0x2C, [0x06])
            sleep(0.5)
            # Read data back from 0x00(00), 6 bytes
            # cTemp MSB, cTemp LSB, cTemp CRC, Humididty MSB, Humidity LSB, Humidity CRC
            data = self._bus.read_i2c_block_data(self._i2c_address, 0x00, 6)
            # Convert the data
            cTemp = round(((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45, 2)
            humidity = round(100 * (data[3] * 256 + data[4]) / 65535.0, 2)
            self._temp, self._hum = cTemp,humidity
        except:
            raise Exception("Could not read the dongle, is it attached?")

    @property
    def temperature(self):
        self._update_temp_hum()
        return self._temp
    
    @property
    def humidity(self):
        self._update_temp_hum()
        return self._hum

    def led_on(self):
        self._green.on()
        self._yellow.on()
        self._red.on()

    def led_off(self):
        self._green.off()
        self._yellow.off()
        self._red.off()
        
    def led_blink(self):
        self._green.off()
        self._yellow.off()
        self._red.on()
        sleep(1.0)
        self._yellow.on()
        self._green.off()
        self._red.off()
        sleep(1.0)
        self._yellow.off()
        self._green.on()
        self._red.off()
        sleep(1.0)

if __name__ == "__main__":
    sensor=SHT30_dongle()
    sensor.led_blink()
    #with open(args.loc+".txt","a") as file: 
    #    file.write(sensor.log_clima())
