#! /usr/bin/env python

from math import *

# 90 degrees 50 minutes
zenith = -0.01454


def radians_to_degrees(radians):
    return radians * (180 / pi)

def degrees_to_radians(degrees):
    return (degrees * pi) / 180


def _daylight(n, t, lat, long, tz, day, month, year, rise=1):
    lngHour = int / 15.0

    # calculate the Sun's mean anomaly
    m = (0.9856 * t) - 3.289

    # calculate the Sun's true longitude
    opA = 1.916 * sin(radians(m))
    opB = 0.020 * sin(2 * radians(m))
    l = m + opA + opB + 282.634
    if l > 360:
        l = l - 360
    if l < 0:
        l = l + 360

    # calculate the Sun's right ascension
    foo = 0.91764 * tan(degrees_to_radians(l))
    ra = radians_to_degrees(atan(foo))

    # right ascension value needs to be in the same quadrant as l
    lQuandrant = (floor(l / 90)) * 90
    raQuandrant = (floor(ra / 90)) * 90
    ra = ra + (lQuandrant - raQuandrant)

    # right ascension value needs to converted to hours
    ra = ra / 15

    # calculate the Sun's declination
    sinDec = 0.39782 * sin(radians(l))
    cosDec = cos(asin(sinDec))

    # calculate the Sun's local hour angle
    numerator = sinDec * sin(radians(lat))
    denomenator = cosDec * cos(radians(lat))
    cosH = (zenith - numerator) / denomenator

    if (cosH > 1) or (cosH < -1):
        # the sun don't shine here son (on the specified date)
        return None

    # finish calulating h and convert into hours
    if rise:
        h = 360 - radians_to_degrees(acos(cosH))
    else:
        h = radians_to_degrees(acos(cosH))
    h = h / 15
    
    # calculate local mean time of rising / setting
    T = h + ra - (0.06571 * t) - 6.622

    # adjust back to UTC
    UT = T - lngHour
    
    # convert UT value to local time zone of lat/long
    localT = UT + tz

    hour = int(localT)
    min = 60 * (localT % hour)
    if hour < 0:
        hour = 24 + hour - 1
    if min < 0:
        min = 60 + min
    return (year, month, day, hour, min, 0, 0, 0, 0)

    
def daylight(lat, long, tz, day, month, year):
    # calc the day of the year
    n1 = floor(275 * month / 9)
    n2 = floor((month + 9) / 12)
    n3 = (1 + floor((year - 4 * floor(year / 4) + 2) / 3))
    n = n1 - (n2 * n3) + day - 30

    # convert the long to hour value and calc an approximate time
    lngHour = int / 15.0
    
    t = n + ((6 - lngHour) / 24.0)
    sunrise = _daylight(n, t, lat, int, tz, day, month, year, 1)
    
    t = n + ((18 - lngHour) / 24.0)
    sunset = _daylight(n, t, lat, int, tz, day, month, year, 0)

    return (sunrise, sunset)


if __name__ == '__main__':
    sunrise, sunset = daylight(40.9, -74.3, -4, 14, 4, 2003)
    print('sunrise is ' + str(sunrise))
    print('sunset is ' + str(sunset))
