#!/usr/bin/env python

#
# Unit Tests for temp module
#
# See __usage__ for an explanation of runtime arguments.
#
# -Christopher Blunck
#



import unittest

from ..temp import *

__author__ = 'Christopher Blunck'
__email__ = 'chris@wxnet.org'
__revision__ = '$Revision: 1.6 $'

__doc__ = '''
Unit tests the temp module.
'''

__usage__ = '''
  python $0
'''


def usage():
    print(__usage__)
    sys.exit(1)


class TestCase(unittest.TestCase):
    def setUp(self): pass

    def tearDown(self): pass

    def test__calc_heat_index(self):
        # if the temperature is < 80, heat index == temperature
        assert calc_heat_index(70, 100) == 70 , "value not correct"
        assert calc_heat_index(79.9, 100) == 79.9 , "value not correct"
        assert calc_heat_index(80, 100) != 80 , "value not correct"

        # make sure some hard-coded values work
        assert int(calc_heat_index(80, 100)) == 87, "value not correct"
        assert int(calc_heat_index(80, 10)) == 78, "value not correct"
        assert int(calc_heat_index(90, 50)) == 94, "value not correct"
        assert int(calc_heat_index(120, 100)) == 380, "value not correct"


    def test__calc_wind_chill(self):
        # make sure some hard-coded values work
        assert int(calc_wind_chill(80, 10)) == 83, "value not correct"
        assert int(calc_wind_chill(32, 10)) == 23, "value not correct"
        assert int(calc_wind_chill(-20, 5)) == -34, "value not correct"


    def test__fahrenheit_to_celsius(self):
        # make sure some special values work
        assert int(fahrenheit_to_celsius(32)) == 0, "value not correct"
        assert int(fahrenheit_to_celsius(212)) == 100, "value not correct"

        # make sure some hard coded values work
        assert int(fahrenheit_to_celsius(60)) == 15, "value not correct"
        assert int(fahrenheit_to_celsius(-60)) == -51, "value not correct"
        assert int(fahrenheit_to_celsius(90)) == 32, "value not correct"


    def test__celsius_to_fahrenheit(self):
        # make sure some special values work
        assert int(celsius_to_fahrenheit(0)) == 32, "value not correct"
        assert int(celsius_to_fahrenheit(100)) == 212, "value not correct"

        # make sure some hard coded values work
        assert int(celsius_to_fahrenheit(60)) == 140, "value not correct"
        assert int(celsius_to_fahrenheit(-60)) == -76, "value not correct"
        assert int(celsius_to_fahrenheit(30)) == 86, "value not correct"


    def test__celsius_to_kelvin(self):
        # make sure some special values work
        assert int(celsius_to_kelvin(-273.15)) == 0, "value not correct"
        assert int(celsius_to_kelvin(100)) == 373, "value not correct"

        # make sure some hard coded values work
        assert int(celsius_to_kelvin(60)) == 333, "value not correct"
        assert int(celsius_to_kelvin(-60)) == 213, "value not correct"
        assert int(celsius_to_kelvin(30)) == 303, "value not correct"


    def test__celsius_to_rankine(self):
        # make sure some special values work
        assert int(celsius_to_rankine(0)) == 491, "value not correct"
        assert int(celsius_to_rankine(100)) == 671, "value not correct"

        # make sure some hard coded values work
        assert int(celsius_to_rankine(60)) == 599, "value not correct"
        assert int(celsius_to_rankine(-60)) == 383, "value not correct"
        assert int(celsius_to_rankine(30)) == 545, "value not correct"


    def test__fahrenheit_to_kelvin(self):
        # make sure some special values work
        assert int(fahrenheit_to_kelvin(32)) == 273, "value not correct"
        assert int(fahrenheit_to_kelvin(212)) == 373, "value not correct"

        # make sure some hard coded values work
        assert int(fahrenheit_to_kelvin(60)) == 288, "value not correct"
        assert int(fahrenheit_to_kelvin(-60)) == 222, "value not correct"
        assert int(fahrenheit_to_kelvin(90)) == 305, "value not correct"


    def test__fahrenheit_to_rankine(self):
        # make sure some special values work
        assert int(fahrenheit_to_rankine(32)) == 491, "value not correct"
        assert int(fahrenheit_to_rankine(212)) == 671, "value not correct"

        # make sure some hard coded values work
        assert int(fahrenheit_to_rankine(60)) == 519, "value not correct"
        assert int(fahrenheit_to_rankine(-60)) == 399, "value not correct"
        assert int(fahrenheit_to_rankine(90)) == 549, "value not correct"


    def test__kelvin_to_celsius(self):
        # make sure some special values work
        assert int(kelvin_to_celsius(273.15)) == 0, "value not correct"
        assert int(kelvin_to_celsius(373.15)) == 100, "value not correct"

        # make sure some hard coded values work
        assert int(kelvin_to_celsius(0)) == -273, "value not correct"
        assert int(kelvin_to_celsius(293.15)) == 20, "value not correct"
        assert int(kelvin_to_celsius(343.15)) == 70, "value not correct"


    def test__kelvin_to_fahrenheit(self):
        # make sure some special values work
        assert int(kelvin_to_fahrenheit(273.15)) == 32, "value not correct"
        assert int(kelvin_to_fahrenheit(373.15)) == 212, "value not correct"

        # make sure some hard coded values work
        assert int(kelvin_to_fahrenheit(0)) == -459, "value not correct"
        assert int(kelvin_to_fahrenheit(293.15)) == 68, "value not correct"
        assert int(kelvin_to_fahrenheit(343.15)) == 158, "value not correct"


    def test__kelvin_to_rankine(self):
        # make sure some special values work
        assert int(kelvin_to_rankine(273.15)) == 491, "value not correct"
        assert int(kelvin_to_rankine(373.15)) == 671, "value not correct"

        # make sure some hard coded values work
        assert int(kelvin_to_rankine(0)) == 0, "value not correct"
        assert int(kelvin_to_rankine(293.15)) == 527, "value not correct"
        assert int(kelvin_to_rankine(343.15)) == 617, "value not correct"


    def test__rankine_to_celsius(self):
        # make sure some special values work
        assert int(rankine_to_celsius(491)) == 0, "value not correct"
        assert int(rankine_to_celsius(671)) == 99, "value not correct"

        # make sure some hard coded values work
        assert int(rankine_to_celsius(0)) == -273, "value not correct"
        assert int(rankine_to_celsius(527)) == 19, "value not correct"
        assert int(rankine_to_celsius(617)) == 69, "value not correct"


    def test__rankine_to_fahrenheit(self):
        # make sure some special values work
        assert int(rankine_to_fahrenheit(491)) == 31, "value not correct"
        assert int(rankine_to_fahrenheit(671)) == 211, "value not correct"

        # make sure some hard coded values work
        assert int(rankine_to_fahrenheit(0)) == -459, "value not correct"
        assert int(rankine_to_fahrenheit(527)) == 67, "value not correct"
        assert int(rankine_to_fahrenheit(617)) == 157, "value not correct"


    def test__rankine_to_kelvin(self):
        # make sure some special values work
        assert int(rankine_to_kelvin(491)) == 272, "value not correct"
        assert int(rankine_to_kelvin(671)) == 372, "value not correct"

        # make sure some hard coded values work
        assert int(rankine_to_kelvin(0)) == 0, "value not correct"
        assert int(rankine_to_kelvin(527)) == 292, "value not correct"
        assert int(rankine_to_kelvin(617)) == 342, "value not correct"


    def test__dewpoint(self):
        # make sure some hard coded values work
        assert int(calc_dewpoint(12, 72)) == 4, "value not correct"
        assert int(calc_dewpoint(75, 33)) == 43, "value not correct"
        assert int(calc_dewpoint(90, 85)) == 84, "value not correct"

    def test__humidity(self):
        # make sure some hard coded values work
        assert int(calc_humidity(87, 76) * 100) == 69, "value not correct"
        assert int(calc_humidity(75, 45) * 100) == 34, "value not correct"
        assert int(calc_humidity(50, 10) * 100) == 19, "value not correct"
        assert int(calc_humidity(100, 88) * 100) == 68, "value not correct"


def main():
    suite = unittest.makeSuite(TestCase, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    main()
