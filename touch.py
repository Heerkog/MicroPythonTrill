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

# Implements a helper class to obtain Trill sensor touches
# Generic Touches class
class Touches(object):

    # Converts data read using MODE_CENTROID to a list of touches
    # Please instantiate subclasses only
    def __init__(self, data):
        self.touches = []

    # Returns a list of touches as tuples, with
    #  (vertical position, touch size) in case of one-directional data, or
    #  (horizontal position, vertical position, horizontal size, vertical size)
    #  in case of two-directional data
    def getTouches(self):
        return self.touches

    # Returns the number of touches
    def getNumTouches(self):
        return len(self.touches)

    # Returns the touch at index as a tuple
    def getTouch(self, index):
        touch = None
        if index < len(self.touches):
            touch = self.touches[index]
        return touch

    # Returns True if no touches are registered
    def isEmpty(self):
        return len(self.touches) == 0


# Touches given one-directional data, e.g., using Bar, Ring, or Craft
class Touches1D(Touches):

    def __init__(self, data):
        super(Touches1D, self).__init__(data)

        verticalLocations = data[:int(len(data)/2)]
        verticalSizes = data[int(len(data)/2):]

        self.touches = []
        for i in range[0:len(verticalLocations)]:
            if verticalLocations[i] is not -1:
                self.touches.append((verticalLocations[i], verticalSizes[i]))


# Touches given two-directional data, e.g., using Square or Hex
class Touches2D(Touches):

    def __init__(self, data):
        super(Touches2D, self).__init__(data)

        vertical = data[:int(len(data)/2)]
        horizontal = data[int(len(data)/2):]

        verticalLocations = vertical[:int(len(vertical)/2)]
        verticalSizes = vertical[int(len(vertical)/2):]

        horizontalLocations = horizontal[:int(len(horizontal)/2)]
        horizontalSizes = horizontal[int(len(horizontal)/2):]

        self.touches = []
        for i in range(0,len(verticalLocations)):
            if verticalLocations[i] is not -1:
                self.touches.append((horizontalLocations[i], verticalLocations[i], horizontalSizes[i], verticalSizes[i]))

