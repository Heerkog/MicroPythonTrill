## MicroPython Trill Sensor Library
This library offers implementations of [Bela](https://bela.io/) 's [Trill touch sensors](https://bela.io/products/trill/) for MicroPython.

## Example usage

```
from machine import SoftI2C, Pin
from trill import Square
from touch import Touches2D

i2c = SoftI2C(scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400000)

square = Square(i2c)

data = square.read()
touches = Touches2D(data)

for touch in touches.getTouches():
    print(touch)
```

## Library functionality
The library consists of two python files with the following classes:

The file `trill.py` consists of the following six classes with functions:

* `TrillSensor` The generic Trill sensor representation, with functions:
  * `__init__(i2c, address, mode, sleep=10)` Initializes a generic Trill sensor using the I<sup>2</sup>C bus `i2c`, the I<sup>2</sup>C address `address`, the mode `mode`, and a sleep time between I<sup>2</sup>C commands of `10` ms.
  * `identify()` Ask the sensor to identify itself and read its type and firmware version.
  * `getType()` Get the sensor type.
  * `getFirmwareVersion()` Get the sensor firmware version.
  * `getSize()` Get the size of the sensor as a tuple (x, y).
  * `getNumChannels()` Get the number of channels of the sensor.
  * `read()` Read the latest scan value from the sensor.
  * `setMode(mode)` Set the sensor mode, as either `trill.MODE_CENTROID`, `trill.MODE_RAW`, `trill.MODE_BASELINE`, or `trill.MODE_DIFF`.
  * `getMode()` Get the sensor mode. Returns `None` if mode hasn't been set.
  * `setScanSettings(speed=0, resolution=12)` Set the scan speed and resolution (numBits) of the sensor, with speed being a value from 0 to 3, and resolution being a value from 9 to 16.body
  * `updateBaseline()` Update the baseline capacitance values of the sensor.
  * `setPrescaler(prescaler=8)` Set the prescaler of the sensor, with prescaler being a value from 1 to 8.
  * `setNoiseThreshold(threshold)` Set the noise threshold for the `trill.MODE_CENTROID` and `trillMODE_DIFF` modes, with threshold being a value from 0 to 255.
  * `setIDACValue(value)` Set the IDAC value of the sensor, with value being a value from 0 to 255.
  * `setMinimumTouchSize(self, minSize)` Set the minimum registered touch size.
  * `setAutoScanInterval(interval=1)` Set the automatic scan interval (used with the EVT pin).
  * `is1D()` Returns `True` if the sensor is one-directional.
  * `is2D()` Returns `True` if the sensor is two-directional.
* `Bar` Subclass of `TrillSensor`, implements a Trill Bar sensor.
    * `__init__(i2c, address=0x20, mode=MODE_CENTROID, sleep=10)` Initializes a Trill Bar sensor using the I<sup>2</sup>C bus `i2c`, the I<sup>2</sup>C address `0x20`, the mode `trill.MODE_CENTROID`, and a sleep time between I<sup>2</sup>C commands of `10` ms.
* `Square` Subclass of `TrillSensor`, implements a Trill Square sensor.
    * `__init__(i2c, address=0x28, mode=MODE_CENTROID, sleep=10)` Initializes a Trill Square sensor using the I<sup>2</sup>C bus `i2c`, the I<sup>2</sup>C address `0x28`, the mode `trill.MODE_CENTROID`, and a sleep time between I<sup>2</sup>C commands of `10` ms.
* `Craft` Subclass of `TrillSensor`, implements a Trill Craft sensor.
    * `__init__(i2c, address=0x30, mode=MODE_CENTROID, sleep=10)` Initializes a Trill Bar sensor using the I<sup>2</sup>C bus `i2c`, the I<sup>2</sup>C address `0x30`, the mode `trill.MODE_CENTROID`, and a sleep time between I<sup>2</sup>C commands of `10` ms.
* `Ring` Subclass of `TrillSensor`, implements a Trill Ring sensor.
    * `__init__(i2c, address=0x38, mode=MODE_CENTROID, sleep=10)` Initializes a Trill Bar sensor using the I<sup>2</sup>C bus `i2c`, the I<sup>2</sup>C address `0x38`, the mode `trill.MODE_CENTROID`, and a sleep time between I<sup>2</sup>C commands of `10` ms.
* `Hex` Subclass of `TrillSensor`, implements a Trill Hex sensor.
    * `__init__(i2c, address=0x40, mode=MODE_CENTROID, sleep=10)` Initializes a Trill Bar sensor using the I<sup>2</sup>C bus `i2c`, the I<sup>2</sup>C address `0x40`, the mode `trill.MODE_CENTROID`, and a sleep time between I<sup>2</sup>C commands of `10` ms.

The file `touch.py` consists of the following three classes with functions:

* `Touches` Implements a helper class to obtain Trill sensor touches from `trill.MODE_CENTROID` data.
  * `__init__(data)` Converts data read using `trill.MODE_CENTROID` to a list of touches
  * `getTouches()` Returns a list of touches as tuples.
  * `getNumTouches()` Returns the number of touches registered.
  * `getTouch(index)` Returns the touch at `index` as a tuple.
  * `isEmpty()` Returns `True` if no touches are registered.
    
* `Touches1D` Subclass of `Touches`, interprets `trill.MODE_CENTROID` data from one-directional sensors.
  * `__init__(data)` Converts one-directional data read using MODE_CENTROID to a list of touches
  * `getTouches()` Returns a list of touches as tuples `[(vertical position, touch size), ...]`.
  * `getTouch(index)` Returns the touch at `index` as a tuple `(vertical position, touch size)`.
* `Touches2D` Subclass of `Touches`, interprets `trill.MODE_CENTROID` data from two-directional sensors.
  * `__init__(data)` Converts two-directional data read using MODE_CENTROID to a list of touches  
  * `getTouches()` Returns a list of touches as tuples `[(horizontal position, vertical position, horizontal size, vertical size), ...]`.
  * `getTouch(index)` Returns the touch at `index` as a tuple `(horizontal position, vertical position, horizontal size, vertical size)`.

