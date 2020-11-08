#!/usr/bin/env python

#
# Unit Tests for pressure module
#
# See __usage__ for an explanation of runtime arguments.
#
# -Christopher Blunck
#


import unittest

from ..pressure import *

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

    def test__atm_to_in32(self):
        # make sure some hard-coded values work
        assert round(atm_to_in32(1.0364), 4) == 31.0104, "value not correct"
        assert round(atm_to_in32(1.0000), 4) == 29.9213, "value not correct"
        assert round(atm_to_in32(0.9268), 4) == 27.7311, "value not correct"
        assert round(atm_to_in32(0.8883), 4) == 26.5791, "value not correct"

    def test__atm_to_in60(self):
        # make sure some hard-coded values work
        assert round(atm_to_in60(1.0364), 4) == 31.0980, "value not correct"
        assert round(atm_to_in60(1.0000), 4) == 30.0058, "value not correct"
        assert round(atm_to_in60(0.9268), 4) == 27.8094, "value not correct"
        assert round(atm_to_in60(0.8883), 4) == 26.6542, "value not correct"

    def test__atm_to_mb(self):
        # make sure some hard-coded values work
        assert round(atm_to_mb(1.0364), 4) == 1050.1323, "value not correct"
        assert round(atm_to_mb(1.0000), 4) == 1013.2500, "value not correct"
        assert round(atm_to_mb(0.9268), 4) == 939.0801, "value not correct"
        assert round(atm_to_mb(0.8883), 4) == 900.0700, "value not correct"

    def test__atm_to_pa(self):
        # make sure some hard-coded values work
        assert round(atm_to_pa(1.0364), 4) == 105013.2300, "value not correct"
        assert round(atm_to_pa(1.0000), 4) == 101325.0000, "value not correct"
        assert round(atm_to_pa(0.9268), 4) == 93908.0100, "value not correct"
        assert round(atm_to_pa(0.8883), 4) == 90006.9975, "value not correct"

    def test__atm_to_lb_sqin(self):
        # make sure some hard-coded values work
        assert round(atm_to_lb_sqin(1.0364), 4) == 15.2309, "value not correct"
        assert round(atm_to_lb_sqin(1.0000), 4) == 14.6960, "value not correct"
        assert round(atm_to_lb_sqin(0.9268), 4) == 13.6203, "value not correct"
        assert round(atm_to_lb_sqin(0.8883), 4) == 13.0545, "value not correct"

    def test__in32_to_mb(self):
        # make sure some hard-coded values work
        assert int(in32_to_mb(31.01)) == 1050, "value not correct"
        assert int(in32_to_mb(29.92)) == 1013, "value not correct"
        assert int(in32_to_mb(27.73)) == 939, "value not correct"
        assert int(in32_to_mb(26.58)) == 900, "value not correct"

    def test__in32_to_atm(self):
        # make sure some hard-coded values work
        assert round(in32_to_atm(31.01), 4) == 1.0364, "value not correct"
        assert round(in32_to_atm(29.92), 4) == 1.0000, "value not correct"
        assert round(in32_to_atm(27.73), 4) == 0.9268, "value not correct"
        assert round(in32_to_atm(26.58), 4) == 0.8883, "value not correct"

    def test__in32_to_lbs(self):
        # make sure some hard-coded values work
        assert round(in32_to_lbs(31.01), 4) == 15.2306, "value not correct"
        assert round(in32_to_lbs(29.92), 4) == 14.6952, "value not correct"
        assert round(in32_to_lbs(27.73), 4) == 13.6196, "value not correct"
        assert round(in32_to_lbs(26.58), 4) == 13.0548, "value not correct"

    def test__in60_to_mb(self):
        # make sure some hard-coded values work
        assert int(in60_to_mb(31.01)) == 1047, "value not correct"
        assert int(in60_to_mb(29.92)) == 1010, "value not correct"
        assert int(in60_to_mb(27.73)) == 936, "value not correct"
        assert int(in60_to_mb(26.58)) == 897, "value not correct"

    def test__in60_to_atm(self):
        # make sure some hard-coded values work
        assert round(in60_to_atm(31.01), 4) == 1.0335, "value not correct"
        assert round(in60_to_atm(29.92), 4) == 0.9971, "value not correct"
        assert round(in60_to_atm(27.73), 4) == 0.9242, "value not correct"
        assert round(in60_to_atm(26.58), 4) == 0.8858, "value not correct"

    def test__in60_to_lbs(self):
        # make sure some hard-coded values work
        assert round(in60_to_lbs(31.01), 4) == 15.1878, "value not correct"
        assert round(in60_to_lbs(29.92), 4) == 14.6539, "value not correct"
        assert round(in60_to_lbs(27.73), 4) == 13.5813, "value not correct"
        assert round(in60_to_lbs(26.58), 4) == 13.0181, "value not correct"

    def test__mb_to_atm(self):
        # make sure some hard-coded values work
        assert round(mb_to_atm(1050), 4) == 1.0363, "value not correct"
        assert round(mb_to_atm(1013), 4) == 0.9998, "value not correct"
        assert round(mb_to_atm(939), 4) == 0.9267, "value not correct"
        assert round(mb_to_atm(900), 4) == 0.8882, "value not correct"

    def test__mb_to_hpa(self):
        # make sure some hard-coded values work
        assert mb_to_hpa(1050) == 1050, "value not correct"
        assert mb_to_hpa(1013) == 1013, "value not correct"
        assert mb_to_hpa(939) == 939, "value not correct"
        assert mb_to_hpa(900) == 900, "value not correct"

    def test__mb_to_in32(self):
        # make sure some hard-coded values work
        assert round(mb_to_in32(1050), 4) == 31.0065, "value not correct"
        assert round(mb_to_in32(1013), 4) == 29.9139, "value not correct"
        assert round(mb_to_in32(939), 4) == 27.7287, "value not correct"
        assert round(mb_to_in32(900), 4) == 26.5770, "value not correct"

    def test__mb_to_in60(self):
        # make sure some hard-coded values work
        assert round(mb_to_in60(1050), 4) == 31.0905, "value not correct"
        assert round(mb_to_in60(1013), 4) == 29.9949, "value not correct"
        assert round(mb_to_in60(939), 4) == 27.8038, "value not correct"
        assert round(mb_to_in60(900), 4) == 26.6490, "value not correct"

    def test__mb_to_kpa(self):
        # make sure some hard-coded values work
        assert round(mb_to_kpa(1050), 4) == 105.0000, "value not correct"
        assert round(mb_to_kpa(1013), 4) == 101.3000, "value not correct"
        assert round(mb_to_kpa(939), 4) == 93.9000, "value not correct"
        assert round(mb_to_kpa(900), 4) == 90.0000, "value not correct"

    def test__mb_to_mm32(self):
        # make sure some hard-coded values work
        assert round(mb_to_mm32(1050), 4) == 787.5630, "value not correct"
        assert round(mb_to_mm32(1013), 4) == 759.8108, "value not correct"
        assert round(mb_to_mm32(939), 4) == 704.3063, "value not correct"
        assert round(mb_to_mm32(900), 4) == 675.0540, "value not correct"

    def test__mb_to_mm60(self):
        # make sure some hard-coded values work
        assert round(mb_to_mm60(1050), 4) == 789.7890, "value not correct"
        assert round(mb_to_mm60(1013), 4) == 761.9583, "value not correct"
        assert round(mb_to_mm60(939), 4) == 706.2970, "value not correct"
        assert round(mb_to_mm60(900), 4) == 676.9620, "value not correct"

    def test__mb_to_n_sqm(self):
        # make sure some hard-coded values work
        assert mb_to_n_sqm(1050) == 105000, "value not correct"
        assert mb_to_n_sqm(1013) == 101300, "value not correct"
        assert mb_to_n_sqm(939) == 93900, "value not correct"
        assert mb_to_n_sqm(900) == 90000, "value not correct"

    def test__mb_to_pa(self):
        # make sure some hard-coded values work
        assert mb_to_pa(1050) == 105000, "value not correct"
        assert mb_to_pa(1013) == 101300, "value not correct"
        assert mb_to_pa(939) == 93900, "value not correct"
        assert mb_to_pa(900) == 90000, "value not correct"

    def test__mb_to_lb_sqft(self):
        # make sure some hard-coded values work
        assert round(mb_to_lb_sqft(1050), 4) == 2192.9702, "value not correct"
        assert round(mb_to_lb_sqft(1013), 4) == 2115.6941, "value not correct"
        assert round(mb_to_lb_sqft(939), 4) == 1961.1419, "value not correct"
        assert round(mb_to_lb_sqft(900), 4) == 1879.6887, "value not correct"

    def test__mb_to_lb_sqin(self):
        # make sure some hard-coded values work
        assert round(mb_to_lb_sqin(1050), 4) == 15.2290, "value not correct"
        assert round(mb_to_lb_sqin(1013), 4) == 14.6923, "value not correct"
        assert round(mb_to_lb_sqin(939), 4) == 13.6191, "value not correct"
        assert round(mb_to_lb_sqin(900), 4) == 13.0534, "value not correct"

    def test__mm32_to_mb(self):
        # make sure some hard-coded values work
        assert round(mm32_to_mb(787), 4) == 1049.2441, "value not correct"
        assert round(mm32_to_mb(759), 4) == 1011.9140, "value not correct"
        assert round(mm32_to_mb(704), 4) == 938.5869, "value not correct"
        assert round(mm32_to_mb(675), 4) == 899.9235, "value not correct"

    def test__mm60_to_mb(self):
        # make sure some hard-coded values work
        for p, expected in [(787, 1046.2929),
                            (759, 1009.0677),
                            (704, 935.9469),
                            (675, 897.3923)]:
            self.assertAlmostEqual(
                mm60_to_mb(p),
                expected,
                places=4,
                msg=f"Incorrect conversion for {p}")

    def test__n_sqm_to_mb(self):
        # make sure some hard-coded values work
        assert n_sqm_to_mb(105000) == 1050, "value not correct"
        assert n_sqm_to_mb(101300) == 1013, "value not correct"
        assert n_sqm_to_mb(93900) == 939, "value not correct"
        assert n_sqm_to_mb(90000) == 900, "value not correct"

    def test__pa_to_atm(self):
        # make sure some hard-coded values work
        assert round(pa_to_atm(105000), 4) == 1.0362, "value not correct"
        assert round(pa_to_atm(101300), 4) == 0.9997, "value not correct"
        assert round(pa_to_atm(93900), 4) == 0.9267, "value not correct"
        assert round(pa_to_atm(90000), 4) == 0.8882, "value not correct"

    def test__pa_to_mb(self):
        # make sure some hard-coded values work
        assert pa_to_mb(105000) == 1050, "value not correct"
        assert pa_to_mb(101300) == 1013, "value not correct"
        assert pa_to_mb(93900) == 939, "value not correct"
        assert pa_to_mb(90000) == 900, "value not correct"

    def test__hpa_to_mb(self):
        # make sure some hard-coded values work
        assert hpa_to_mb(1050) == 1050, "value not correct"
        assert hpa_to_mb(1013) == 1013, "value not correct"
        assert hpa_to_mb(939) == 939, "value not correct"
        assert hpa_to_mb(900) == 900, "value not correct"

    def test__kpa_to_mb(self):
        # make sure some hard-coded values work
        assert kpa_to_mb(1050) == 10500, "value not correct"
        assert kpa_to_mb(1013) == 10130, "value not correct"
        assert kpa_to_mb(939) == 9390, "value not correct"
        assert kpa_to_mb(900) == 9000, "value not correct"

    def test__lb_sqft_to_mb(self):
        # make sure some hard-coded values work
        assert round(lb_sqft_to_mb(2192), 4) == 1049.5362, "value not correct"
        assert round(lb_sqft_to_mb(2115), 4) == 1012.6683, "value not correct"
        assert round(lb_sqft_to_mb(1961), 4) == 938.9327, "value not correct"
        assert round(lb_sqft_to_mb(1879), 4) == 899.6708, "value not correct"

    def test__lb_sqin_to_atm(self):
        # make sure some hard-coded values work
        assert round(lb_sqin_to_atm(15.2310), 4) == 1.0364, "value not correct"
        assert round(lb_sqin_to_atm(14.6960), 4) == 1.0000, "value not correct"
        assert round(lb_sqin_to_atm(13.6203), 4) == 0.9268, "value not correct"
        assert round(lb_sqin_to_atm(13.0545), 4) == 0.8883, "value not correct"

    def test__lb_sqin_to_mm32(self):
        # make sure some hard-coded values work
        assert round(lb_sqin_to_mm32(15.2310), 4) == 31.0106, \
            "value not correct"
        assert round(lb_sqin_to_mm32(14.6960), 4) == 29.9213, \
            "value not correct"
        assert round(lb_sqin_to_mm32(13.6203), 4) == 27.7312, \
            "value not correct"
        assert round(lb_sqin_to_mm32(13.0545), 4) == 26.5792, \
            "value not correct"

    def test__lb_sqin_to_mm60(self):
        # make sure some hard-coded values work
        assert round(lb_sqin_to_mm60(15.2310), 4) == 31.0982, \
            "value not correct"
        assert round(lb_sqin_to_mm60(14.6960), 4) == 30.0059, \
            "value not correct"
        assert round(lb_sqin_to_mm60(13.6203), 4) == 27.8095, \
            "value not correct"
        assert round(lb_sqin_to_mm60(13.0545), 4) == 26.6543, \
            "value not correct"

    def test__lb_sqin_to_mb(self):
        # make sure some hard-coded values work
        assert round(lb_sqin_to_mb(15.2310), 4) == 1050.1386, \
            "value not correct"
        assert round(lb_sqin_to_mb(14.6960), 4) == 1013.2517, \
            "value not correct"
        assert round(lb_sqin_to_mb(13.6203), 4) == 939.0849, \
            "value not correct"
        assert round(lb_sqin_to_mb(13.0545), 4) == 900.0745, \
            "value not correct"


def main():
    suite = unittest.makeSuite(TestCase, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
