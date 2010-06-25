from __future__ import absolute_import

import unittest
from mock import Mock, patch_object

from ..davis import VProCRC, VantagePro, LoopStruct

loop_data = "4c4f4f14003e032175da0239d10204056301ffffffffffffffffffff" \
    "ffffffffff4effffffffffffff0000ffff7f0000ffff000000000000000000000000ffff" \
    "ffffffffff0000000000000000000000000000000000002703064b26023e070a0d1163"

class TestCRC(unittest.TestCase):

    def test_crc(self):
        raw = loop_data.decode('hex')
        result = VProCRC.verify( raw )
        self.assertTrue(result)


class TestParse(unittest.TestCase):
    cmd_mock = Mock()   # for mocking '_cmd' method in 'vp'
    loop_mock = Mock()  # for mocking '_loop_cmd' method in 'vp'

    def test_unpack_loop_data(self):
        LoopStruct.unpack(loop_data.decode('hex'))

    @patch_object(VantagePro, '_cmd', cmd_mock )
    @patch_object(VantagePro, '_loop_cmd', loop_mock )
    def test_fields(self):
        self.loop_mock.return_value = loop_data.decode('hex')
        vp = VantagePro('/dev/ttyS0')
        fields = vp._get_loop_fields()

        self.assertAlmostEquals( fields['Pressure'], 29.98499999 )
        self.assertAlmostEquals( fields['TempIn'], 73.0 )
        self.assertEquals( fields['HumIn'], 57 )
        self.assertAlmostEquals( fields['TempOut'], 72.09999999999 )
        self.assertEquals( fields['WindSpeed'], 4 )
        self.assertEquals( fields['WindSpeed10Min'], 5 )
        self.assertEquals( fields['WindDir'], 355 )
        self.assertEquals( fields['HumOut'], 78 )
        self.assertEquals( fields['RainRate'], 0.0 )
        self.assertEquals( fields['UV'], 0xFF )
        self.assertEquals( fields['SolarRad'], 0x7FFF )
        self.assertEquals( fields['RainStorm'], 0 )
        self.assertEquals( fields['StormStartDate'], '2127-15-31' )
        self.assertEquals( fields['RainDay'], 0 )
        self.assertEquals( fields['RainMonth'], 0 )
        self.assertEquals( fields['RainYear'], 0 )
        self.assertEquals( fields['ETDay'], 0 )
        self.assertEquals( fields['ETMonth'], 0 )
        self.assertEquals( fields['ETYear'], 0 )
        self.assertEquals( fields['SoilMoist'], (0xFF,0xFF,0xFF,0xFF) )
        self.assertEquals( fields['LeafWetness'], (0xFF,0xFF,0xFF,0) )
        self.assertEquals( fields['BatteryStatus'], 0 )
        self.assertAlmostEquals( fields['BatteryVolts'], 4.728515625 )
        self.assertEquals( fields['ForecastIcon'], 6 )
        self.assertEquals( fields['ForecastRuleNo'], 75 )
        self.assertEquals( fields['SunRise'], '05:50' )
        self.assertEquals( fields['SunSet'], '18:54' )

    @patch_object(VantagePro, '_cmd', cmd_mock )
    @patch_object(VantagePro, '_loop_cmd', loop_mock )
    def test_derived_fields(self):
        self.loop_mock.return_value = loop_data.decode('hex')
        vp = VantagePro('/dev/ttyS0')
        fields = vp._get_loop_fields()
        vp._calc_derived_fields(fields)

        self.assertAlmostEquals( fields['HeatIndex'], 72.09999999)
        self.assertAlmostEquals( fields['WindChill'], 74.17574285)
        self.assertAlmostEquals( fields['DewPoint'],  64.97343800)
        self.assertNotEquals( fields['DateStamp'], '' )
        self.assertTrue( fields['Year'] > 2000 )
        self.assertTrue( 1 <= int(fields['Month']) <= 12 )
        self.assertNotEquals( fields['DateStampUtc'], '' )
        self.assertTrue( fields['YearUtc'] > 2000 )
        self.assertTrue( 1 <= int(fields['MonthUtc']) <= 12 )


# vim: sts=4:ts=4:sw=4
