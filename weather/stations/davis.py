from weather.units import *

import serial, binascii, time, array


class VantagePro:
    '''
    A class capable of reading raw (binary) weather data from a
    vantage pro console and parsing it into usable scalar
    (integer/long/real) values.

    The data read from the console is in binary format, and must be
    converted to hex using a least-ordered nybble strategy.  The hex
    is in fixed-length format, and values can be extracted using an
    offset and length strategy (e.g. outside humidity starts at
    position 56 and is 2 bytes long).
    
    '''

    def __init__(self, device, start='c4f4f4'):
        self.start = start
        self.device = device

    def _read(self):
        '''
        reads a raw string containing data read from the device
        provided (in /dev/XXX) format.  this method blocks until a
        complete string is read from the device.
        '''
        
        ser = serial.Serial(self.device, 19200, timeout=0)
        ser.write('\n')
        time.sleep(1)
        ser.write('LOOP 1\n')
        time.sleep(1)
        line = ser.read(512)
        
        if len(line) > 20:
            self.raw = line
        else:
            self.raw = self._read()

    def _hexify(self):
        # convert the binary into hex using low-ordered nybble format
        cooked = self.raw.encode("hex")
        cooked = array.array('H', cooked)
        cooked.byteswap()
        cooked = cooked.tostring()

        # the data before start is garbage
        cooked = cooked.split(self.start)[1]

        # strip off the first 4 bytes, which indicate the loop response
        self.data = cooked[4:]


    def parse(self):
        '''
        read and parse a set of data read from the console.  after the
        data is parsed it is available in the fields variable.
        '''
        
        # read the raw data
        self._read()

        # convert the raw data into a hex format we can work with
        self._hexify()

        # this dict will hold all of our values
        fields = {}
        
        # parse the easy fields
        fields['Pressure'] = self.get_field(4, 4) / 1000.0
        fields['TempIn'] = self.get_field(8, 4) / 10.0
        fields['HumIn'] = self.get_field(12, 2)
        fields['TempOut'] = self.get_field(14, 4) / 10.0
        fields['WindSpeed'] = self.get_field(18, 2)
        fields['WindSpeed10Min'] = self.get_field(20, 2)
        fields['WindDir'] = self.get_field(22, 4)
        fields['HumOut'] = self.get_field(56, 2)
        fields['RainRate'] = self.get_field(72, 4) / 100.0
        fields['UV'] = self.get_field(76, 2)
        fields['SolarRad'] = self.get_field(78, 4)
        fields['RainStorm'] = self.get_field(82, 4) / 100.0
        
        # stormstartdate (4 bytes)
        date = self.get_field(86, 4)
        year = (date & 0x7f) + 2000
        date = date >> 7
        day = date & 0x1f
        date = date >> 5
        month = date
        fields['StormStartDate'] = "%s-%s-%s" % (year, month, day)

        # rain totals
        fields['RainDay'] = self.get_field(90, 4) / 100.0
        fields['RainMonth'] = self.get_field(94, 4) / 100.0
        fields['RainYear'] = self.get_field(98, 4) / 100.0

        # evapotranspiration totals
        fields['ETDay'] = self.get_field(116, 4)
        fields['ETMonth'] = self.get_field(120, 4)
        fields['ETYear'] = self.get_field(124, 4)
        
        # soil moisture (array of length 4, 2 bytes each)
        fields['SoilMoist'] = []
        for pos in range(0, 4):
            fields['SoilMoist'].append(self.get_field(120 + (2 * pos), 2))
            
        # leaf wetness (array of length 4, 2 bytes each)
        fields['LeafWetness'] = []
        for pos in range(0, 4):
            fields['LeafWetness'].append(self.get_field(128 + (2 * pos), 2))

        # battery statistics
        fields['BatteryStatus'] = self.get_field(162, 2)
        fields['BatteryCounts'] = self.get_field(164, 4)

        # forecast candy
        fields['ForecastIcon'] = self.get_field(168, 2)
        fields['ForecastRuleNo'] = self.get_field(170, 2)
        
        # sunrise (4 bytes)
        # format: HHMM, and space padded on the left.
        # example: "601" is 6:01 AM
        sunrise = self.get_field(172, 4)
        sunrise = str(sunrise).zfill(4)
        fields['SunRise'] = "%s:%s" % (sunrise[:2], sunrise[2:])
        
        # sunset (4 bytes).  same as above
        sunset = self.get_field(176, 4)
        sunset = str(sunset).zfill(4)
        fields['SunSet'] = "%s:%s" % (sunset[:2], sunset[2:])

        # calculate the derived fields (windchill, dewpoint, heat index)
        self._calc_derived_fields(fields)

        # set the fields variable the the values in the dict 
        self.fields = fields

        
    def _calc_derived_fields(self, fields):
        '''
        calculates the derived fields (those fields that are calculated)
        '''
        
        # convenience variables for the calculations below
        temp = fields['TempOut']
        hum = fields['HumOut']
        wind = fields['WindSpeed']
        wind10min = fields['WindSpeed10Min']
        
        fields['HeatIndex'] = calc_heat_index(temp, hum)
        fields['WindChill'] = calc_wind_chill(temp, wind, wind10min)
        fields['DewPoint'] = calc_dewpoint(temp, hum)

        now = time.localtime()
        fields['DateStamp'] = time.strftime("%y-%m-%d %H:%M:%S", now)
        fields['Year'] = now[0]
        fields['Month'] = str(now[1]).zfill(2)
        


    def get_field(self, start, len):
        '''
        returns the value in the field specified by the starting
        offset and of the length provided.  this value is computed by
        first reversing the hex data, followed by conversion of the
        hex data to a long.
        '''
        
        field = self.data[start:start + len]
        inverted = field[::-1]
        return long(inverted, 16)
        
