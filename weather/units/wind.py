#!/usr/bin/env python

#
# See __doc__ for an explanation of what this module does
#
# See __usage__ for an explanation of runtime arguments.
#
# -Christopher Blunck
#

import sys

__author__ = 'Christopher Blunck'
__email__ = 'chris@wxnet.org'
__revision__ = '$Revision: 1.6 $'

__doc__ = 'wind related conversion functions'
__usage__ = 'this module should not be run via the command line'


def knots_to_ft_sec(kts):
    """Knots (kt) to feet/second (ft/s)"""
    return kts * 1.6878099


def knots_to_km_hr(kts):
    """Knots (kt) to kilometers/hour (kph)"""
    return kts * 1.852


def knots_to_m_sec(kts):
    """Knots (kt) to meters/second (m/s)"""
    return kts * 0.514444


def knots_to_mph(kts):
    """Knots (kt) to miles/hour (mph)"""
    return kts * 1.1507794


def knots_to_nmph(kts):
    """Knots (kt) to nautical miles/hour (nmph)"""
    return kts


def ft_sec_to_knots(ft):
    """Feet/second (ft/s) to knots (kt)"""
    return ft * 0.5924838


def km_hr_to_knots(km):
    """Kilometers/hour (kph) to knots (kt)"""
    return km * 0.5399568


def m_sec_to_knots(m):
    """Meters/second (m/s) to knots (kt)"""
    return m * 1.943846


def mph_to_knots(mph):
    """Miles/hour (mph) to knots (kt)"""
    return mph * 0.86897624


def nmph_to_knots(mph):
    """Nautical miles/hour (nmph) to knots (kt)"""
    return mph


def mph_to_ft_min(mph):
    """Miles/hour (mph) to feet/minute (ft/min)"""
    return mph * 88


def mph_to_ft_sec(mph):
    """Miles/hour (mph) to feet/second (ft/s)"""
    return mph * 1.466666


def mph_to_km_hr(mph):
    """Miles/hour (mph) to kilometers/hour (kph)"""
    return mph * 1.609344


def mph_to_m_sec(mph):
    """Miles/hour (mph) to meters/second (m/s)"""
    return mph * 0.44704


def ft_min_to_mph(ft):
    """Feet/minute (ft/min) to miles/hour (mph)"""
    return ft * 0.01136363


def ft_sec_to_knots(ft):
    """Feet/second (ft/s) to knots (kt)"""
    return ft * 0.5924838


def ft_sec_to_mph(ft):
    """Feet/second (ft/s) to miles/hour (mph)"""
    return ft * 0.681818


def km_hr_to_knots(km):
    """Kilometers/hour (kph) to knots (kt)"""
    return km * 0.5399568


def km_hr_to_mph(km):
    """Kilometers/hour (kph) to miles/hour (mph)"""
    return km * 0.62137119


def m_sec_to_knots(m):
    """Meters/second (m/s) to knots (kt)"""
    return m * 1.943846


def m_sec_to_mph(m):
    """Meters/second (m/s) to miles/hour (mph)"""
    return m * 2.2369363
