<div id="top"></div>


<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL License][license-shield]][license-url]
[![Website][website-shield]][website-url]



<!-- PROJECT HEADER -->
<br />
<div align="center">
<h3 align="center">MicroPython Trill Sensor Library</h3>

  <p align="center">
    This library offers implementations of Bela's Trill touch sensors for MicroPython.
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
This library offers implementations of [Bela](https://bela.io/) 's [Trill touch sensors](https://bela.io/products/trill/) for MicroPython.
The library has been tested using an ESP32 development board ([TinyPICO](https://tinypico.com)).

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy simply clone this repository.

   ```sh
   git clone https://github.com/heerkog/MicroPythonTrill.git
   ```

The repository is structured as followed:

* `LICENSE` the license.
* `readme.md`
* `touch.py` touch helper classes.
* `trill.py` the library classes.

Example implementation:

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

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

The library consists of two python files with the following classes:

The file `trill.py` consists of the following six classes with functions:

* `TrillSensor` The generic Trill sensor representation, with functions:
  * `__init__(i2c, address, mode, sleep=10)` Initializes a generic Trill sensor using the I<sup>2</sup>C bus `i2c`, the I<sup>2</sup>C address `address`, the mode `mode`, and a sleep time between I<sup>2</sup>C commands of `10` ms.
  * `identify()` Ask the sensor to identify itself and read its type and firmware version.
  * `get_type()` Get the sensor type.
  * `get_firmware_version()` Get the sensor firmware version.
  * `get_size()` Get the size of the sensor as a tuple (x, y).
  * `get_num_channels()` Get the number of channels of the sensor.
  * `read()` Read the latest scan value from the sensor.
  * `set_mode(mode)` Set the sensor mode, as either `trill.MODE_CENTROID`, `trill.MODE_RAW`, `trill.MODE_BASELINE`, or `trill.MODE_DIFF`.
  * `get_mode()` Get the sensor mode. Returns `None` if mode hasn't been set.
  * `set_scan_settings(speed=0, resolution=12)` Set the scan speed and resolution (numBits) of the sensor, with speed being a value from 0 to 3, and resolution being a value from 9 to 16.body
  * `update_baseline()` Update the baseline capacitance values of the sensor.
  * `set_prescaler(prescaler=8)` Set the prescaler of the sensor, with prescaler being a value from 1 to 8.
  * `set_noise_threshold(threshold)` Set the noise threshold for the `trill.MODE_CENTROID` and `trill.MODE_DIFF` modes, with threshold being a value from 0 to 255.
  * `set_IDAC_value(value)` Set the IDAC value of the sensor, with value being a value from 0 to 255.
  * `set_minimum_touch_size(self, minSize)` Set the minimum registered touch size.
  * `set_auto_scan_interval(interval=1)` Set the automatic scan interval (used with the EVT pin).
  * `is_1D()` Returns `True` if the sensor is one-directional.
  * `is_2D()` Returns `True` if the sensor is two-directional.
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
  * `get_touches()` Returns a list of touches as tuples.
  * `get_num_touches()` Returns the number of touches registered.
  * `get_touch(index)` Returns the touch at `index` as a tuple.
  * `is_empty()` Returns `True` if no touches are registered.
* `Touches1D` Subclass of `Touches`, interprets `trill.MODE_CENTROID` data from one-directional sensors.
  * `__init__(data)` Converts one-directional data read using MODE_CENTROID to a list of touches
  * `get_touches()` Returns a list of touches as tuples `[(vertical position, touch size), ...]`.
  * `get_touch(index)` Returns the touch at `index` as a tuple `(vertical position, touch size)`.
* `Touches2D` Subclass of `Touches`, interprets `trill.MODE_CENTROID` data from two-directional sensors.
  * `__init__(data)` Converts two-directional data read using MODE_CENTROID to a list of touches
  * `get_touches()` Returns a list of touches as tuples `[(horizontal position, vertical position, horizontal size, vertical size), ...]`.
  * `get_touch(index)` Returns the touch at `index` as a tuple `(horizontal position, vertical position, horizontal size, vertical size)`.



<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU General Public License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Heerko Groefsema - [@heerkog](https://twitter.com/heerkog)

Project Link: [https://github.com/heerkog/MicroPythonTrill](https://github.com/heerkog/MicroPythonTrill)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
The following resources were of interest during development:

* [About Trill](https://learn.bela.io/products/trill/about-trill/)
* [Trill Arduino](https://github.com/BelaPlatform/Trill-Arduino)  
* [Mikes Pi Bakery](https://github.com/Grumpy-Mike/Mikes-Pi-Bakery)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/heerkog/MicroPythonTrill.svg?style=for-the-badge
[contributors-url]: https://github.com/heerkog/MicroPythonTrill/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/heerkog/MicroPythonTrill.svg?style=for-the-badge
[forks-url]: https://github.com/heerkog/MicroPythonTrill/network/members
[stars-shield]: https://img.shields.io/github/stars/heerkog/MicroPythonTrill.svg?style=for-the-badge
[stars-url]: https://github.com/heerkog/MicroPythonTrill/stargazers
[issues-shield]: https://img.shields.io/github/issues/heerkog/MicroPythonTrill.svg?style=for-the-badge
[issues-url]: https://github.com/heerkog/MicroPythonTrill/issues
[license-shield]: https://img.shields.io/github/license/heerkog/MicroPythonTrill.svg?style=for-the-badge
[license-url]: https://github.com/heerkog/MicroPythonTrill/blob/master/LICENSE.txt

[website-shield]: https://img.shields.io/badge/Website-H-black.svg?style=for-the-badge&colorB=2A638C
[website-url]: https://hgroefsema.nl
