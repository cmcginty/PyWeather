#!/usr/bin/env python

#
# Unit Tests for pressure module
#
# See __usage__ for an explanation of runtime arguments.
#
# -Christopher Blunck
#



import unittest

from ..wind import *

__author__ = 'Christopher Blunck'
__email__ = 'chris@wxnet.org'
__revision__ = '$Revision: 1.6 $'

__doc__ = '''
Unit tests the pressure module.
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


    def test__knots_to_ft_sec(self):
        # make sure some hard-coded values work
        assert round(knots_to_ft_sec(5), 4) == 8.4390, "value not correct"
        assert round(knots_to_ft_sec(14), 4) == 23.6293, "value not correct"
        assert round(knots_to_ft_sec(35), 4) == 59.0733, "value not correct"
        assert round(knots_to_ft_sec(70), 4) == 118.1467, "value not correct"


    def test__knots_to_km_hr(self):
        # make sure some hard-coded values work
        assert round(knots_to_km_hr(5), 4) == 9.2600, "value not correct"
        assert round(knots_to_km_hr(14), 4) == 25.9280, "value not correct"
        assert round(knots_to_km_hr(35), 4) == 64.8200, "value not correct"
        assert round(knots_to_km_hr(70), 4) == 129.6400, "value not correct"


    def test__knots_to_m_sec(self):
        # make sure some hard-coded values work
        assert round(knots_to_m_sec(5), 4) == 2.5722, "value not correct"
        assert round(knots_to_m_sec(14), 4) == 7.2022, "value not correct"
        assert round(knots_to_m_sec(35), 4) == 18.0055, "value not correct"
        assert round(knots_to_m_sec(70), 4) == 36.0111, "value not correct"


    def test__knots_to_mph(self):
        # make sure some hard-coded values work
        assert round(knots_to_mph(5), 4) == 5.7539, "value not correct"
        assert round(knots_to_mph(14), 4) == 16.1109, "value not correct"
        assert round(knots_to_mph(35), 4) == 40.2773, "value not correct"
        assert round(knots_to_mph(70), 4) == 80.5546, "value not correct"


    def test__knots_to_nmph(self):
        # make sure some hard-coded values work
        assert round(knots_to_nmph(5), 4) == 5, "value not correct"
        assert round(knots_to_nmph(14), 4) == 14, "value not correct"
        assert round(knots_to_nmph(35), 4) == 35, "value not correct"
        assert round(knots_to_nmph(70), 4) == 70, "value not correct"


    def test__ft_sec_to_knots(self):
        # make sure some hard-coded values work
        assert round(ft_sec_to_knots(8.4390), 4) == 5, "value not correct"
        assert round(ft_sec_to_knots(23.6293), 4) == 14, "value not correct"
        assert round(ft_sec_to_knots(59.0733), 4) == 35, "value not correct"
        assert round(ft_sec_to_knots(118.1467), 4) == 70, "value not correct"


    def test__km_hr_to_knots(self):
        # make sure some hard-coded values work
        assert round(km_hr_to_knots(9.2600), 4) == 5, "value not correct"
        assert round(km_hr_to_knots(25.9280), 4) == 14, "value not correct"
        assert round(km_hr_to_knots(64.8200), 4) == 35, "value not correct"
        assert round(km_hr_to_knots(129.6400), 4) == 70, "value not correct"


    def test__m_sec_to_knots(self):
        # make sure some hard-coded values work
        assert round(m_sec_to_knots(2.5722), 4) == 5, "value not correct"
        assert round(m_sec_to_knots(7.2022), 4) == 14, "value not correct"
        assert round(m_sec_to_knots(18.0055), 4) == 34.9999, "value not correct"
        assert round(m_sec_to_knots(36.0111), 4) == 70, "value not correct"


    def test__mph_to_knots(self):
        # make sure some hard-coded values work
        assert round(mph_to_knots(5.7539), 4) == 5, "value not correct"
        assert round(mph_to_knots(16.1109), 4) == 14, "value not correct"
        assert round(mph_to_knots(40.2773), 4) == 35, "value not correct"
        assert round(mph_to_knots(80.5546), 4) == 70, "value not correct"


    def test__nmph_to_knots(self):
        # make sure some hard-coded values work
        assert round(nmph_to_knots(5), 4) == 5, "value not correct"
        assert round(nmph_to_knots(14), 4) == 14, "value not correct"
        assert round(nmph_to_knots(35), 4) == 35, "value not correct"
        assert round(nmph_to_knots(70), 4) == 70, "value not correct"


    def test__mph_to_ft_min(self):
        # make sure some hard-coded values work
        assert round(mph_to_ft_min(5), 4) == 440, "value not correct"
        assert round(mph_to_ft_min(16), 4) == 1408, "value not correct"
        assert round(mph_to_ft_min(40), 4) == 3520, "value not correct"
        assert round(mph_to_ft_min(80), 4) == 7040, "value not correct"


    def test__mph_to_ft_sec(self):
        # make sure some hard-coded values work
        assert round(mph_to_ft_sec(5), 4) == 7.3333, "value not correct"
        assert round(mph_to_ft_sec(16), 4) == 23.4667, "value not correct"
        assert round(mph_to_ft_sec(40), 4) == 58.6666, "value not correct"
        assert round(mph_to_ft_sec(80), 4) == 117.3333, "value not correct"


    def test__mph_to_km_hr(self):
        # make sure some hard-coded values work
        assert round(mph_to_km_hr(5), 4) == 8.0467, "value not correct"
        assert round(mph_to_km_hr(16), 4) == 25.7495, "value not correct"
        assert round(mph_to_km_hr(40), 4) == 64.3738, "value not correct"
        assert round(mph_to_km_hr(80), 4) == 128.7475, "value not correct"


    def test__mph_to_m_sec(self):
        # make sure some hard-coded values work
        assert round(mph_to_m_sec(5), 4) == 2.2352, "value not correct"
        assert round(mph_to_m_sec(16), 4) == 7.1526, "value not correct"
        assert round(mph_to_m_sec(40), 4) == 17.8816, "value not correct"
        assert round(mph_to_m_sec(80), 4) == 35.7632, "value not correct"


    def test__ft_min_to_mph(self):
        # make sure some hard-coded values work
        assert round(ft_min_to_mph(440), 4) == 5, "value not correct"
        assert round(ft_min_to_mph(1408), 4) == 16, "value not correct"
        assert round(ft_min_to_mph(3520), 4) == 40, "value not correct"
        assert round(ft_min_to_mph(7040), 4) == 80, "value not correct"


    def test__ft_sec_to_knots(self):
        # make sure some hard-coded values work
        assert round(ft_sec_to_knots(8.4390), 4) == 5, "value not correct"
        assert round(ft_sec_to_knots(23.6293), 4) == 14, "value not correct"
        assert round(ft_sec_to_knots(59.0733), 4) == 35, "value not correct"
        assert round(ft_sec_to_knots(118.1467), 4) == 70, "value not correct"


    def test__ft_sec_to_mph(self):
        # make sure some hard-coded values work
        assert round(ft_sec_to_mph(7.3333), 4) == 5, "value not correct"
        assert round(ft_sec_to_mph(23.4667), 4) == 16, "value not correct"
        assert round(ft_sec_to_mph(58.6666), 4) == 39.9999, "value not correct"
        assert round(ft_sec_to_mph(117.3333), 4) == 80, "value not correct"


    def test__km_hr_to_knots(self):
        # make sure some hard-coded values work
        assert round(km_hr_to_knots(9.2600), 4) == 5, "value not correct"
        assert round(km_hr_to_knots(25.9280), 4) == 14, "value not correct"
        assert round(km_hr_to_knots(64.8200), 4) == 35, "value not correct"
        assert round(km_hr_to_knots(129.6400), 4) == 70, "value not correct"


    def test__km_hr_to_mph(self):
        # make sure some hard-coded values work
        assert round(km_hr_to_mph(8.0467), 4) == 5, "value not correct"
        assert round(km_hr_to_mph(25.7495), 4) == 16, "value not correct"
        assert round(km_hr_to_mph(64.3738), 4) == 40, "value not correct"
        assert round(km_hr_to_mph(128.7475), 4) == 80, "value not correct"


    def test__m_sec_to_knots(self):
        # make sure some hard-coded values work
        assert round(m_sec_to_knots(2.5722), 4) == 5, "value not correct"
        assert round(m_sec_to_knots(7.2022), 4) == 14, "value not correct"
        assert round(m_sec_to_knots(18.0055), 4) == 34.9999, "value not correct"
        assert round(m_sec_to_knots(36.0111), 4) == 70, "value not correct"


    def test__m_sec_to_mph(self):
        # make sure some hard-coded values work
        assert round(m_sec_to_mph(2.2352), 4) == 5, "value not correct"
        assert round(m_sec_to_mph(7.1526), 4) == 15.9999, "value not correct"
        assert round(m_sec_to_mph(17.8816), 4) == 40, "value not correct"
        assert round(m_sec_to_mph(35.7632), 4) == 80, "value not correct"


def main():
    suite = unittest.makeSuite(TestCase, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    main()
