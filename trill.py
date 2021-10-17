# MicroPython Trill Sensor library
# Copyright (C) 2021 H. Groefsema
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Implements an I2C Trill sensor
import time
import struct

REG_COMMAND = 0x00
REG_DATA = 0x04

COMMAND_NONE = 0x00
COMMAND_MODE = 0x01
COMMAND_SCAN_SETTINGS = 0x02
COMMAND_PRESCALER = 0x03
COMMAND_NOISE_THRESHOLD = 0x04
COMMAND_IDAC = 0x05
COMMAND_BASELINE_UPDATE = 0x06
COMMAND_MINIMUM_SIZE = 0x07
COMMAND_AUTO_SCAN_INTERVAL = 0x10
COMMAND_IDENTIFY = 0xFF

MODE_CENTROID = 0x00
MODE_RAW = 0x01
MODE_BASELINE = 0x02
MODE_DIFF = 0x03

TYPES = ["Unknown", "Bar", "Square", "Craft", "Ring", "Hex", "Flex"]

# Class that represents a generic Trill sensor
class TrillSensor(object):

    # Initialize a generic Trill sensor, with
    #  i2c being an I2C bus instance
    #  address being the I2C address of the sensor,
    #  mode being the sensor mode, and
    #  sleep being the delay to use between I2C bus communication
    def __init__(self, i2c, address=0x00, mode=None, sleep=10):
        self.i2c = i2c
        self.address=address
        self.mode = mode
        self.sleep = sleep
        self.type = 0
        self.identifiedType = 0
        self.firmware = None
        self.size = (1, 1)
        self.channels = 0
        self.maxTouches = 0
        self.directions = 0

    # Ask the sensor to identify itself and read its type and firmware version
    def identify(self):
        self.i2c.writeto(self.address, struct.pack("1B", REG_DATA))
        time.sleep_ms(10)
        self.i2c.writeto_mem(self.address, REG_COMMAND, struct.pack("1B", COMMAND_IDENTIFY))
        time.sleep_ms(self.sleep + 15)
        (_, self.identifiedType, self.firmware) = self.i2c.readfrom(self.address, 3)
        print("Trill type", TYPES[self.identifiedType], "with firmware version", self.firmware)
        if self.type is not self.identifiedType:
            print("Warning: connected Trill device does not identify as", TYPES[self.type], "!!!")

    # Get the sensor type
    def get_type(self):
        if self.identifiedType is 0:
            self.identify()
        return TYPES[self.identifiedType]

    # Get the sensor firmware version
    def get_firmware_version(self):
        if self.firmware is None:
            self.identify()
        return self.firmware

    # Get the size of the sensor as a tuple (x, y)
    def get_size(self):
        return self.size

    # Get the number of channels of the sensor
    def get_num_channels(self):
        return self.channels

    # Read the latest scan value from the sensor
    def read(self):
        self.i2c.writeto(self.address, struct.pack("1B", REG_DATA))
        time.sleep_ms(self.sleep)

    # Set the sensor mode
    def set_mode(self, mode):
        self.mode = mode
        self.i2c.writeto_mem(self.address, REG_COMMAND, struct.pack("2B", COMMAND_MODE, mode))
        time.sleep_ms(self.sleep)

    # Get the sensor mode
    # Returns None if mode hasn't been set
    def get_mode(self):
        return self.mode

    # Set the scan speed and resolution (numBits) of the sensor, with
    #  speed being a value from 0 to 3, and
    #  resolution being a value from 9 to 16
    def set_scan_settings(self, speed=0, resolution=12):
        if speed < 0:
            speed = 0
        elif speed > 3:
            speed = 3

        if resolution < 9:
            resolution = 9
        elif resolution > 16:
            resolution = 16

        self.i2c.writeto_mem(self.address, REG_COMMAND, struct.pack("3B", COMMAND_SCAN_SETTINGS, speed, resolution))
        time.sleep_ms(self.sleep)

    # Update the baseline capacitance values of the sensor
    def update_baseline(self):
        self.i2c.writeto_mem(self.address, REG_COMMAND, struct.pack("1B", COMMAND_BASELINE_UPDATE))
        time.sleep_ms(self.sleep)

    # Set the prescaler of the sensor, with
    #  prescaler being a value from 1 to 8
    def set_prescaler(self, prescaler=8):
        self.i2c.writeto_mem(self.address, REG_COMMAND, struct.pack("2B", COMMAND_PRESCALER, prescaler))
        time.sleep_ms(self.sleep)

    # Set the noise threshold for the MODE_CENTROID and MODE_DIFF modes, with
    #  threshold being a value from 0 to 255
    def set_noise_threshold(self, threshold):
        self.i2c.writeto_mem(self.address, REG_COMMAND, struct.pack("2B", COMMAND_NOISE_THRESHOLD, threshold))
        time.sleep_ms(self.sleep)

    # Set the IDAC value of the sensor, with
    #  value being a value from 0 to 255
    def set_IDAC_value(self, value):
        self.i2c.writeto_mem(self.address, REG_COMMAND, struct.pack("2B", COMMAND_IDAC, value))
        time.sleep_ms(self.sleep)

    # Set the minimum registered touch size
    def set_minimum_touch_size(self, minSize):
        self.i2c.writeto_mem(self.address, REG_COMMAND, struct.pack("BH", COMMAND_MINIMUM_SIZE, minSize))
        time.sleep_ms(self.sleep)

    # Set the automatic scan interval (used with the EVT pin)
    def set_auto_scan_interval(self, interval=1):
        self.i2c.writeto_mem(self.address, REG_COMMAND, struct.pack("2B", COMMAND_AUTO_SCAN_INTERVAL, interval))
        time.sleep_ms(self.sleep)

    # Returns True if the sensor is one-directional
    def is_1D(self):
        return self.directions is 1

    # Returns True if the sensor is two-directional
    def is_2D(self):
        return self.directions is 2


# Class representing a Trill Bar
class Bar(TrillSensor):

    def __init__(self, i2c, address=0x20, mode=MODE_CENTROID, sleep=10):
        super(Bar, self).__init__(i2c, address, mode, sleep)
        self.type = 1
        self.size = (1, 3200)
        self.channels = 26
        self.maxTouches = 5
        self.directions = 1

        self.set_mode(mode)
        self.set_scan_settings()
        self.update_baseline()

    def read(self):
        super(Bar, self).read()
        data = None

        if self.mode is MODE_CENTROID:
            data = struct.unpack(">10h", self.i2c.readfrom_mem(self.address, REG_DATA, 4 * self.maxTouches))
        else:
            data = struct.unpack(">26h", self.i2c.readfrom_mem(self.address, REG_DATA, 2 * self.channels))

        return data


# Class representing a Trill Square
class Square(TrillSensor):

    def __init__(self, i2c, address=0x28, mode=MODE_CENTROID, sleep=10):
        super(Square, self).__init__(i2c, address, mode, sleep)
        self.type = 2
        self.size = (1792, 1792)
        self.channels = 30
        self.maxTouches = 4
        self.directions = 2

        self.set_mode(mode)
        self.set_scan_settings()
        self.update_baseline()

    def read(self):
        super(Square, self).read()
        data = None

        if self.mode is MODE_CENTROID:
            data = struct.unpack(">16h", self.i2c.readfrom_mem(self.address, REG_DATA, 4 * self.directions * self.maxTouches))
        else:
            data = struct.unpack(">30h", self.i2c.readfrom_mem(self.address, REG_DATA, 2 * self.channels))

        return data


# Class representing a Trill Craft
class Craft(TrillSensor):

    def __init__(self, i2c, address=0x30, mode=MODE_CENTROID, sleep=10):
        super(Craft, self).__init__(i2c, address, mode, sleep)
        self.type = 3
        self.size = (1, 4096)
        self.channels = 30
        self.maxTouches = 5
        self.directions = 1

        self.set_mode(mode)
        self.set_scan_settings()
        self.update_baseline()

    def read(self):
        super(Craft, self).read()
        data = None

        if self.mode is MODE_CENTROID:
            data = struct.unpack(">10h", self.i2c.readfrom_mem(self.address, REG_DATA, 4 * self.maxTouches))
        else:
            data = struct.unpack(">26h", self.i2c.readfrom_mem(self.address, REG_DATA, 2 * self.channels))

        return data


# Class representing a Trill Ring
class Ring(TrillSensor):

    def __init__(self, i2c, address=0x38, mode=MODE_CENTROID, sleep=10):
        super(Ring, self).__init__(i2c, address, mode, sleep)
        self.type = 4
        self.size = (1, 3584)
        self.channels = 28
        self.maxTouches = 5
        self.directions = 1

        self.set_mode(mode)
        self.set_scan_settings()
        self.update_baseline()

    def read(self):
        super(Ring, self).read()
        data = None

        if self.mode is MODE_CENTROID:
            data = struct.unpack(">10h", self.i2c.readfrom_mem(self.address, REG_DATA, 4 * self.maxTouches))
        else:
            data = struct.unpack(">28h", self.i2c.readfrom_mem(self.address, REG_DATA, 2 * self.channels))

        return data


# Class representing a Trill Hex
class Hex(TrillSensor):

    def __init__(self, i2c, address=0x40, mode=MODE_CENTROID, sleep=10):
        super(Hex, self).__init__(i2c, address, mode, sleep)
        self.type = 5
        self.size = (1664, 1920)
        self.channels = 30
        self.maxTouches = 4
        self.directions = 2

        self.set_mode(mode)
        self.set_scan_settings()
        self.update_baseline()

    def read(self):
        super(Hex, self).read()
        data = None

        if self.mode is MODE_CENTROID:
            data = struct.unpack(">16h", self.i2c.readfrom_mem(self.address, REG_DATA, 4 * self.directions * self.maxTouches))
        else:
            data = struct.unpack(">30h", self.i2c.readfrom_mem(self.address, REG_DATA, 2 * self.channels))

        return data
