

import codecs
import datetime
import mock
import unittest

from ..davis import VProCRC, VantagePro, LoopStruct, _fields_to_weather_point
from ..station import WeatherPoint

loop_data = (
    b"4c4f4f14003e032175da0239d10204056301ffffffffffffffffffff"
    b"ffffffffff4effffffffffffff0000ffff7f0000ffff000000000000000000000000ffff"
    b"ffffffffff0000000000000000000000000000000000002703064b26023e070a0d1163")


class TestCRC(unittest.TestCase):

    def test_crc(self):
        raw = codecs.decode(loop_data, 'hex')
        result = VProCRC.verify(raw)
        self.assertTrue(result)


class TestParse(unittest.TestCase):
    cmd_mock = mock.Mock()   # for mocking '_cmd' method in 'vp'
    loop_mock = mock.Mock()  # for mocking '_loop_cmd' method in 'vp'

    def test_unpack_loop_data(self):
        LoopStruct.unpack(codecs.decode(loop_data, 'hex'))

    @mock.patch.object(VantagePro, '_cmd', cmd_mock)
    @mock.patch.object(VantagePro, '_loop_cmd', loop_mock)
    def test_fields(self):
        self.loop_mock.return_value = codecs.decode(loop_data, 'hex')
        # TODO: this is working just if there is an actual weather station attached.
        vp = VantagePro('/dev/ttyUSB0')
        fields = vp._get_loop_fields()

        self.assertAlmostEqual(fields['Pressure'], 29.98499999)
        self.assertAlmostEqual(fields['TempIn'], 73.0)
        self.assertEqual(fields['HumIn'], 57)
        self.assertAlmostEqual(fields['TempOut'], 72.09999999999)
        self.assertEqual(fields['WindSpeed'], 4)
        self.assertEqual(fields['WindSpeed10Min'], 5)
        self.assertEqual(fields['WindDir'], 355)
        self.assertEqual(fields['HumOut'], 78)
        self.assertEqual(fields['RainRate'], 0.0)
        self.assertEqual(fields['UV'], 0xFF)
        self.assertEqual(fields['SolarRad'], 0x7FFF)
        self.assertEqual(fields['RainStorm'], 0)
        self.assertEqual(fields['StormStartDate'], '2127-15-31')
        self.assertEqual(fields['RainDay'], 0)
        self.assertEqual(fields['RainMonth'], 0)
        self.assertEqual(fields['RainYear'], 0)
        self.assertEqual(fields['ETDay'], 0)
        self.assertEqual(fields['ETMonth'], 0)
        self.assertEqual(fields['ETYear'], 0)
        self.assertEqual(fields['SoilMoist'], (0xFF, 0xFF, 0xFF, 0xFF))
        self.assertEqual(fields['LeafWetness'], (0xFF, 0xFF, 0xFF, 0))
        self.assertEqual(fields['BatteryStatus'], 0)
        self.assertAlmostEqual(fields['BatteryVolts'], 4.728515625)
        self.assertEqual(fields['ForecastIcon'], 6)
        self.assertEqual(fields['ForecastRuleNo'], 75)
        self.assertEqual(fields['SunRise'], '05:50')
        self.assertEqual(fields['SunSet'], '18:54')

    @mock.patch.object(VantagePro, '_cmd', cmd_mock)
    @mock.patch.object(VantagePro, '_loop_cmd', loop_mock)
    def test_derived_fields(self):
        self.loop_mock.return_value = codecs.decode(loop_data, 'hex')
        # TODO same as todo above!
        vp = VantagePro('/dev/ttyUSB0')
        fields = vp._get_loop_fields()
        vp._calc_derived_fields(fields)

        self.assertAlmostEqual(fields['HeatIndex'], 72.09999999)
        self.assertAlmostEqual(fields['WindChill'], 74.17574285)
        self.assertAlmostEqual(fields['DewPoint'], 64.97343800)
        self.assertNotEqual(fields['DateStamp'], '')
        self.assertTrue(fields['Year'] > 2000)
        self.assertTrue(1 <= int(fields['Month']) <= 12)
        self.assertNotEqual(fields['DateStampUtc'], '')
        self.assertTrue(fields['YearUtc'] > 2000)
        self.assertTrue(1 <= int(fields['MonthUtc']) <= 12)


class TestFieldsToWeatherPoint(unittest.TestCase):

    def test_fields_to_weather_point(self):
        fields = {
            'TempOut': 87,
            'Pressure': 29.9,
            'DewPoint': 80,
            'HumOut': 56,
            'RainRate': 0.1,
            'RainDay': 0.2,
            'DateStampUtc': '2020-01-02 03:04:05',
            'WindSpeed10Min': 5,
            'WindDir': 15
        }
        expected = WeatherPoint(
            time=datetime.datetime(2020, 1, 2, 3, 4, 5),
            temperature_f=87,
            humidity=56,
            dew_point_f=80,
            pressure=29.9,
            rain_rate_in=0.1,
            rain_day_in=0.2,
            wind_speed_mph=5,
            wind_direction=15
        )
        self.assertEqual(_fields_to_weather_point(fields), expected)


# vim: sts=4:ts=4:sw=4
