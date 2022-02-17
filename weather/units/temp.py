#!/usr/bin/env python

#
# See __doc__ for an explanation of what this module does
#
# See __usage__ for an explanation of runtime arguments.
#
# -Christopher Blunck
#

import math
import sys

__author__ = 'Christopher Blunck'
__email__ = 'chris@wxnet.org'
__revision__ = '$Revision: 1.6 $'

__doc__ = 'temperature related conversion functions'
__usage__ = 'this module should not be run via the command line'


def celsius_to_fahrenheit(c):
    """Degrees Celsius (C) to degrees Fahrenheit (F)"""
    return (c * 1.8) + 32.0


def celsius_to_kelvin(c):
    """Degrees Celsius (C) to degrees Kelvin (K)"""
    return c + 273.15


def celsius_to_rankine(c):
    """Degrees Celsius (C) to degrees Rankine (R)"""
    return (c * 1.8) + 491.67


def fahrenheit_to_celsius(f):
    """Degrees Fahrenheit (F) to degrees Celsius (C)"""
    return (f - 32.0) * 0.555556


def fahrenheit_to_kelvin(f):
    """Degrees Fahrenheit (F) to degrees Kelvin (K)"""
    return (f * 0.555556) + 255.37


def fahrenheit_to_rankine(f):
    """Degrees Fahrenheit (F) to degrees Rankine (R)"""
    return f + 459.67


def kelvin_to_celsius(k):
    """Degrees Kelvin (K) to degrees Celsius (C)"""
    return k - 273.15


def kelvin_to_fahrenheit(k):
    """Degrees Kelvin (K) to degrees Fahrenheit (F)"""
    return (k - 255.37) * 1.8


def kelvin_to_rankine(k):
    """Degrees Kelvin (K) to degrees Rankine (R)"""
    return k * 1.8


def rankine_to_celsius(r):
    """Degrees Rankine (R) to degrees Celsius (C)"""
    return (r - 491.67) * 0.555556


def rankine_to_fahrenheit(r):
    """Degrees Rankine (R) to degrees Fahrenheit (F)"""
    return r - 459.67


def rankine_to_kelvin(r):
    """Degrees Rankine (R) to degrees Kelvin (K)"""
    return r * 0.555556


def calc_heat_index(temp, hum):
    """
    calculates the heat index based upon temperature (in F) and humidity.
    http://www.srh.noaa.gov/bmx/tables/heat_index.html

    returns the heat index in degrees F.
    """

    if temp < 80:
        return temp
    else:
        return -42.379 + 2.04901523 * temp + 10.14333127 * hum - 0.22475541 * \
               temp * hum - 6.83783 * (10 ** -3) * (temp ** 2) - 5.481717 * \
               (10 ** -2) * (hum ** 2) + 1.22874 * (10 ** -3) * (temp ** 2) * \
               hum + 8.5282 * (10 ** -4) * temp * (hum ** 2) - 1.99 * \
               (10 ** -6) * (temp ** 2) * (hum ** 2)


def calc_wind_chill(t, windspeed, windspeed10min=None):
    """
    calculates the wind chill value based upon the temperature (F) and
    wind.

    returns the wind chill in degrees F.
    """

    w = max(windspeed10min or 0, windspeed)
    return 35.74 + 0.6215 * t - 35.75 * (w ** 0.16) + 0.4275 * t * (w ** 0.16)


def calc_humidity(temp, dewpoint):
    """
    calculates the humidity via the formula from weatherwise.org
    return the relative humidity
    """

    t = fahrenheit_to_celsius(temp)
    td = fahrenheit_to_celsius(dewpoint)

    num = 112 - (0.1 * t) + td
    denom = 112 + (0.9 * t)

    rh = math.pow((num / denom), 8)

    return rh


def calc_dewpoint(temp, hum):
    """
    calculates the dewpoint via the formula from weatherwise.org
    return the dewpoint in degrees F.
    """

    c = fahrenheit_to_celsius(temp)
    x = 1 - 0.01 * hum

    dewpoint = (14.55 + 0.114 * c) * x
    dewpoint = dewpoint + ((2.5 + 0.007 * c) * x) ** 3
    dewpoint = dewpoint + (15.9 + 0.117 * c) * x ** 14
    dewpoint = c - dewpoint

    return celsius_to_fahrenheit(dewpoint)


def calc_dewpoint_davis(temp, hum):
    '''
    calculate the dewpoint via the formula used by Davis. See Davis Application Note 28 - Derived Variables in Davis
    Weather Products.
    :author: Paolo Bellagente (p.bellagente@unibs.it - 23/03/2017
    :param temp: Outside temperature in F
    :param hum: Relative outside humidity
    :return: the dewpoint in F
    '''
    v = hum * 0.01 * 6.112 * math.exp((17.62 * temp) / (temp + 243.12))
    n = 243.12 * (math.log(v)) - 440.1
    d = 19.43 - math.log(v)
    return n / d
