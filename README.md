## MicroPython Trill Sensor Library
This library offers implementations of Bela's Trill sensors for MicroPython.

## Example usage

```
from machine import SoftI2C, Pin
from trill import Square
from touch import Touches2D

i2c = SoftI2C(scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400000)

s = Square(i2c)
data = s.read()

t = Touches2D(data)
print(t.getTouches())
```
