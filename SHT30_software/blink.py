#SHT30_Dongle_LEDs

# The dongle has three built in LEDs, green, yellow and red.
# pin 14 is green, 15 is yellow and 18 is red, mapped to raspberry zero pin naming
# pull to ground to switch on the led

#gpio interface for raspberry
from gpiozero import LED
#smbus to interface the SHT30 via I2C
import smbus
from time import sleep



# define the colors
class SHT30_dongle():
    """
    Represents the dedicated Dongle with SHT30 Sensor and 3 LEDs for RPi zero

    The device is compatible to standard RPi zero, thus can be soldered without wires.
    The physical data can be found in the SHT30_sensor folder.
    Included are CAE, CAD and gerber files. 
    """
    def __init__(self,smbus_adress = 1, i2c_address = 0x45):
        self.green = LED(14, active_high = False)
        self.yellow = LED(15, active_high = False)
        self.red = LED(18, active_high = False)
        self.bus = smbus.SMBus(smbus_adress)
        self.i2c_address = i2c_address
        self.update_temp_hum()

    def measure(self):
        # Send measurement command, 0x2C
        #	0x06(06) High repeatability measurement
        self.bus.write_i2c_block_data(self.i2c_address, 0x2C, [0x06])
        sleep(0.5)
        data = self.bus.read_i2c_block_data(self.i2c_address, 0x00, 6)
        cTemp = round(((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45, 2)
        humidity = round(100 * (data[3] * 256 + data[4]) / 65535.0, 2)
        return cTemp, humidity

    def update_temp_hum(self):
        try:
            self._temp, self._hum = self.measure()
        except:
            raise Exception("Could not update")

    @property
    def temperature(self):
        self.update_temp_hum()
        return self._temp
    
    @property
    def humidity(self):
        self.update_temp_hum()
        return self._hum

    def led_on(self):
        self.green(on)
        self.yellow(on)
        self.red(on)

    def led_off(self):
        self.green(off)
        self.yellow(off)
        self.red(off)
        
    def led_blink(self):
        self.green.off()
        self.yellow.off()
        self.red.on()
        sleep(1.0)
        self.yellow.on()
        self.green.off()
        self.red.off()
        sleep(1.0)
        self.yellow.off()
        self.green.on()
        self.red.off()
        sleep(1.0)

if __name__ == "__main__":
    sensor=SHT30_dongle()
    sensor.led_blink()
