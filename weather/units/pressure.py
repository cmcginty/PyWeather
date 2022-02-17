#!/usr/bin/env python

#
# See __doc__ for an explanation of what this module does
#
# See __usage__ for an explanation of runtime arguments.
#
# -Christopher Blunck
#


__author__ = 'Christopher Blunck'
__email__ = 'chris@wxnet.org'
__revision__ = '$Revision: 1.6 $'

__doc__ = 'pressure related conversion functions'
__usage__ = 'this module should not be run via the command line'


def atm_to_in32(atm):
    """Atmospheres (atm) to inches of mercury @32F (inHg32)"""
    return atm * 29.9213


def atm_to_in60(atm):
    """Atmospheres (atm) to inches of mercury @60F (inHg60)"""
    return atm * 30.0058


def atm_to_mb(atm):
    """Atmospheres (atm) to millibars (mb)"""
    return atm * 1013.25


def atm_to_pa(atm):
    """Atmospheres (atm) to pascals (Pa)"""
    return atm * 101325


def atm_to_lb_sqin(atm):
    """Atmospheres (atm) to pounds/square inch (lb/in**2)"""
    return atm * 14.696


def in32_to_mb(inches):
    """Inches of mercury @32F (inHg32) to millibars (mb)"""
    return inches * 33.8639


def in32_to_atm(inches):
    """Inches of mercury @32F (inHg32) to millibars (mb)"""
    return inches * 0.0334211


def in32_to_lbs(inches):
    """Inches of mercury @32F (inHg32) to pounds/square inch (lb/in**2)"""
    return inches * 0.49115


def in60_to_mb(inches):
    """Inches of mercury @60F (inHg60) to atmospheres (atm)"""
    return inches * 33.7685


def in60_to_atm(inches):
    """Inches of mercury @60F (inHg60) to millibars (mb)"""
    return inches * 0.0333269


def in60_to_lbs(inches):
    """Inches of mercury @60F (inHg60) to pounds/square inch (lb/in**2)"""
    return inches * 0.48977


def incConv_to_Pa(inches):
    """
    Inches of mercury to Pascals using the NIST conventional coefficient
    :param inches: inches of mg
    :return: pascals
    """
    return inches * 3.386389


def incConv_to_kPa(inches):
    """
    Inches of mercury to kilo Pascals using the NIST conventional coefficient
    :param inches: inches of mg
    :return: pascals
    """
    return incConv_to_Pa(inches) * 1000


def mb_to_atm(mb):
    """Millibars (mb) to atmospheres (atm)"""
    return mb * 0.000986923


def mb_to_hpa(mb):
    """Millibars (mb) to hectopascals (hPa)"""
    return mb


def mb_to_in32(mb):
    """Millibars (mb) to inches of mercury @32F (inHg60)"""
    return mb * 0.02953


def mb_to_in60(mb):
    """Millibars (mb) to inches of mercury @60F (inHg60)"""
    return mb * 0.02961


def mb_to_kpa(mb):
    """Millibars (mb) to kilopascals (kPa)"""
    return mb * 0.1


def mb_to_mm32(mb):
    """Millibars (mb) to millimeters of mercury @32F (mmHg)"""
    return mb * 0.75006


def mb_to_mm60(mb):
    """Millibars (mb) to millimeters of mercury @60F (mmHg)"""
    return mb * 0.75218


def mb_to_n_sqm(mb):
    """Millibars (mb) to newtons/square meter (N/m**2)"""
    return mb * 100


def mb_to_pa(mb):
    """Millibars (mb) to pascals (Pa)"""
    return mb * 100


def mb_to_lb_sqft(mb):
    """Millibars (mb) to pounds/square foot (lb/ft**2)"""
    return mb * 2.088543


def mb_to_lb_sqin(mb):
    """Millibars (mb) to pounds/square inch (lb/in**2)"""
    return mb * 0.0145038


def mm32_to_mb(mm32):
    """Millimeters of mercury @32F (mmHg) to millibars (mb)"""
    return mm32 * 1.33322


def mm60_to_mb(mm60):
    """Millimeters of mercury @60F (mmHg) to millibars (mb)"""
    return mm60 * 1.32947


def n_sqm_to_mb(nsqm):
    """Newtons/square meter (N/m**2) to millibars (mb)"""
    return nsqm * 0.01


def pa_to_atm(pa):
    """Pascals (Pa) to atmospheres (atm)"""
    return pa * 0.000009869


def pa_to_mb(pa):
    """Pascals (Pa) to millibars (mb)"""
    return pa * 0.01


def hpa_to_mb(hpa):
    """Hectopascals (hPa) to millibars (mb)"""
    return hpa


def kpa_to_mb(hpa):
    """Kilopascals (kPa) to millibars (mb)"""
    return hpa * 10


def lb_sqft_to_mb(lbs):
    """Pounds/square foot (lb/ft**2) to millibars (mb)"""
    return lbs * 0.478803


def lb_sqin_to_atm(lbs):
    """Pounds/square inch (lb/in**2) to atmospheres (atm)"""
    return lbs * 0.068046


def lb_sqin_to_mm32(lbs):
    """Pounds/square inch (lb/in**2) to inches of mercury @32F (inHg32)"""
    return lbs * 2.03602


def lb_sqin_to_mm60(lbs):
    """Pounds/square inch (lb/in**2) to inches of mercury @60F (inHg60)"""
    return lbs * 2.04177


def lb_sqin_to_mb(lbs):
    """Pounds/square inch (lb/in**2) to millibars (mb)"""
    return lbs * 68.9474483


def hpa_to_inches(hpa):
    return hpa / 33.87
