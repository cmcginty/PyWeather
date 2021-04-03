'''Tests for the station module.'''

import unittest

from ..station import WeatherPoint


class WeatherPointTest(unittest.TestCase):

    def test_temperature_conversion(self):
        w_f = WeatherPoint(temperature_f=80)
        self.assertEqual(w_f.temperature_f, 80)
        self.assertAlmostEqual(w_f.temperature_c, 26.666688)

        w_c = WeatherPoint(temperature_c=21)
        self.assertEqual(w_c.temperature_c, 21)
        self.assertAlmostEqual(w_c.temperature_f, 69.8)
