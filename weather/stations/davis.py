'''
Davis Vantage Pro and Pro2 Service

Abstract:
Allows data query of Davis Vantage Pro and Pro2 devices via serial port
interface.  The primary implemented serial commands supported are LOOP and
DMPAFT.

The LOOP command can aquire all real-time data points. The DMPAFT command is
used to aquire periodic high/low data.

All data is returned in a dict structure with value/key pairs. Periodic data is
only captured once per period. When not active, the keys for periodic data are
not present in the results.

Author: Patrick C. McGinty (pyweather@tuxcoder.com)
Date: 2010-06-025

Original Author: Christopher Blunck (chris@wxnet.org)
Date: 2006-03-27
'''

from __future__ import absolute_import

from ._struct import Struct
from ..units import *

import logging
import serial
import struct
import time
from array import array

log = logging.getLogger(__name__)

# public interfaces for module
__all__ = ['VantagePro', 'NoDeviceException' ]

READ_DELAY = 5
BAUD = 19200


def log_raw(msg,raw):
    log.debug( msg + ': ' + raw.encode('hex') )


class NoDeviceException(Exception): pass


class VProCRC(object):
    '''
    Implements CRC algorithm, necessary for encoding and verifying data from
    the Davis Vantage Pro unit.
    '''

    CRC_TABLE = (
        0x0, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
        0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
        0x1231, 0x210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
        0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
        0x2462, 0x3443, 0x420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,
        0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
        0x3653, 0x2672, 0x1611, 0x630, 0x76d7, 0x66f6, 0x5695, 0x46b4,
        0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,
        0x48c4, 0x58e5, 0x6886, 0x78a7, 0x840, 0x1861, 0x2802, 0x3823,
        0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,
        0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0xa50, 0x3a33, 0x2a12,
        0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
        0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0xc60, 0x1c41,
        0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,
        0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0xe70,
        0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,
        0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,
        0x1080, 0xa1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
        0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,
        0x2b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,
        0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
        0x34e2, 0x24c3, 0x14a0, 0x481, 0x7466, 0x6447, 0x5424, 0x4405,
        0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,
        0x26d3, 0x36f2, 0x691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
        0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,
        0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x8e1, 0x3882, 0x28a3,
        0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
        0x4a75, 0x5a54, 0x6a37, 0x7a16, 0xaf1, 0x1ad0, 0x2ab3, 0x3a92,
        0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,
        0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0xcc1,
        0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
        0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0xed1, 0x1ef0,
      )


    @staticmethod
    def get(data):
        '''
        return CRC calc value from raw serial data
        '''
        crc = 0
        for byte in array('B',data):
            crc = (VProCRC.CRC_TABLE[ (crc>>8) ^ byte ] ^ ((crc&0xFF) << 8))
        return crc


    @staticmethod
    def verify(data):
        '''
        perform CRC check on raw serial data, return true if valid.
        a valid CRC == 0.
        '''
        if len(data) == 0:
            return False
        crc = VProCRC.get(data)
        if crc: log.info("CRC Bad")
        else:   log.debug("CRC OK")
        return not crc

# --------------------------------------------------------------------------- #

class LoopStruct( Struct ):
    '''
    For unpacking data structure returned by the 'LOOP' command. this structure
    contains all of the real-time data that can be read from the Davis Vantage
    Pro.
    '''
    FMT = (
        ('LOO',         '3s'), ('BarTrend',    'B'),  ('PacketType',  'B'),
        ('NextRec',      'H'), ('Pressure',    'H'),  ('TempIn',      'H'),
        ('HumIn',        'B'), ('TempOut',     'H'),  ('WindSpeed',   'B'),
        ('WindSpeed10Min','B'),('WindDir',     'H'),  ('ExtraTemps',  '7s'),
        ('SoilTemps',   '4s'), ('LeafTemps',  '4s'),  ('HumOut',      'B'),
        ('HumExtra',    '7s'), ('RainRate',    'H'),  ('UV',          'B'),
        ('SolarRad',     'H'), ('RainStorm',   'H'),  ('StormStartDate','H'),
        ('RainDay',      'H'), ('RainMonth',   'H'),  ('RainYear',    'H'),
        ('ETDay',        'H'), ('ETMonth',     'H'),  ('ETYear',      'H'),
        ('SoilMoist',   '4s'), ('LeafWetness','4s'),  ('AlarmIn',     'B'),
        ('AlarmRain',    'B'), ('AlarmOut' ,  '2s'),  ('AlarmExTempHum','8s'),
        ('AlarmSoilLeaf','4s'),('BatteryStatus','B'), ('BatteryVolts','H'),
        ('ForecastIcon','B'),  ('ForecastRuleNo','B'),('SunRise',     'H'),
        ('SunSet',      'H'),  ('EOL',         '2s'), ('CRC',         'H'),
      )


    def __init__(self):
        super(LoopStruct,self).__init__(self.FMT,'=')


    def _post_unpack(self,items):
        items['Pressure']       = items['Pressure']   / 1000.0
        items['TempIn']         = items['TempIn']     /   10.0
        items['TempOut']        = items['TempOut']    /   10.0
        items['RainRate']       = items['RainRate']   /  100.0
        items['RainStorm']      = items['RainStorm']  /  100.0
        items['StormStartDate'] = self._unpack_storm_date(
                                        items['StormStartDate'])
        # rain totals
        items['RainDay']     = items['RainDay']   /  100.0
        items['RainMonth']   = items['RainMonth'] /  100.0
        items['RainYear']    = items['RainYear']  /  100.0
        # evapotranspiration totals
        items['ETDay']       = items['ETDay']     / 1000.0
        items['ETMonth']     = items['ETMonth']   /  100.0
        items['ETYear']      = items['ETYear']    /  100.0
        # soil moisture + leaf wetness
        items['SoilMoist']   = struct.unpack('4B',items['SoilMoist'])
        items['LeafWetness'] = struct.unpack('4B',items['LeafWetness'])
        # battery statistics
        items['BatteryVolts'] = items['BatteryVolts'] * 300 / 512.0 / 100.0
        # sunrise / sunset
        items['SunRise'] = self._unpack_time( items['SunRise'] )
        items['SunSet']  = self._unpack_time( items['SunSet'] )
        return items


    @staticmethod
    def _unpack_time( val ):
        '''
        given a packed time field, unpack and return "HH:MM" string.
        '''
        # format: HHMM, and space padded on the left.ex: "601" is 6:01 AM
        return "%02d:%02d" % divmod(val,100)  # covert to "06:01"


    @staticmethod
    def _unpack_storm_date( date ):
        '''
        given a packed storm date field, unpack and return 'YYYY-MM-DD' string.
        '''
        year  = (date & 0x7f) + 2000        # 7 bits
        day   = (date >> 7) & 0x01f         # 5 bits
        month = (date >> 12) & 0x0f         # 4 bits
        return "%s-%s-%s" % (year, month, day)

# --------------------------------------------------------------------------- #

class _ArchiveStruct( object ):
    '''
    common features for both Rev.A and Rev.B structures.
    '''
    def __init__(self):
        super(_ArchiveStruct,self).__init__(self.FMT,'=')


    def _post_unpack( self, items ):
        vals = self._unpack_date_time( items['DateStamp'], items['TimeStamp'])
        items.update( zip(('Year','Month','Day','Hour','Min'), vals) )
        items['TempOut']    = items['TempOut']    /   10.0
        items['TempOutHi']  = items['TempOutHi']  /   10.0
        items['TempOutLow'] = items['TempOutLow'] /   10.0
        items['Pressure']   = items['Pressure']   / 1000.0
        items['TempIn']     = items['TempIn']     /   10.0
        items['UV']         = items['UV']         /   10.0
        items['ETHour']     = items['ETHour']     / 1000.0
        items['WindHiDir']  = int(items['WindHiDir']    * 22.5)
        items['WindHiDir']  = int(items['WindAvgDir']   * 22.5)
        items['SoilTemps']  = tuple(
                t-90 for t in struct.unpack('4B',items['SoilTemps']))
        items['ExtraHum']   = struct.unpack('2B',items['ExtraHum'])
        items['SoilMoist']  = struct.unpack('4B',items['SoilMoist'])
        return items


    @staticmethod
    def _unpack_date_time( date, time ):
        day   = date & 0x1f                     # 5 bits
        month = (date >> 5) & 0x0f              # 4 bits
        year  = ((date >> 9) & 0x7f) + 2000     # 7 bits
        hour, min_  = divmod(time,100)
        return (year, month, day, hour, min_)

# --------------------------------------------------------------------------- #

class _ArchiveAStruct( _ArchiveStruct, Struct ):
    FMT = (
        ('DateStamp',   'H'),  ('TimeStamp',   'H'),  ('TempOut',     'H'),
        ('TempOutHi',   'H'),  ('TempOutLow',  'H'),  ('RainRate',    'H'),
        ('RainRateHi',  'H'),  ('Pressure',    'H'),  ('SolarRad',    'H'),
        ('WindSamps',   'H'),  ('TempIn',      'H'),  ('HumIn',       'B'),
        ('HumOut',      'B'),  ('WindAvg',     'B'),  ('WindHi',      'B'),
        ('WindHiDir',   'B'),  ('WindAvgDir',  'B'),  ('UV',          'B'),
        ('ETHour',      'B'),  ('unused',      'B'),  ('SoilMoist',  '4s'),
        ('SoilTemps',  '4s'),  ('LeafWetness','4s'),  ('ExtraTemps', '2s'),
        ('ExtraHum',   '2s'),  ('ReedClosed',  'H'),  ('ReedOpened',  'H'),
        ('unused',      'B'),
      )


    def _post_unpack( self, items ):
        items = super(_ArchiveAStruct,self)._post_unpack( items )
        items['LeafWetness'] = struct.unpack('4B',items['LeafWetness'])
        items['ExtraTemps'] = tuple(
                t-90 for t in struct.unpack('2B',items['ExtraTemps']))
        return items

# --------------------------------------------------------------------------- #

class _ArchiveBStruct( _ArchiveStruct, Struct ):
    FMT = (
        ('DateStamp',   'H'),  ('TimeStamp',   'H'),  ('TempOut',     'H'),
        ('TempOutHi',   'H'),  ('TempOutLow',  'H'),  ('RainRate',    'H'),
        ('RainRateHi',  'H'),  ('Pressure',    'H'),  ('SolarRad',    'H'),
        ('WindSamps',   'H'),  ('TempIn',      'H'),  ('HumIn',       'B'),
        ('HumOut',      'B'),  ('WindAvg',     'B'),  ('WindHi',      'B'),
        ('WindHiDir',   'B'),  ('WindAvgDir',  'B'),  ('UV',          'B'),
        ('ETHour',      'B'),  ('SolarRadHi',  'H'),  ('UVHi',        'B'),
        ('ForecastRuleNo','B'),('LeafTemps',  '2s'),  ('LeafWetness','2s'),
        ('SoilTemps',  '4s'),  ('RecType',     'B'),  ('ExtraHum',   '2s'),
        ('ExtraTemps', '3s'),  ('SoilMoist',  '4s'),
      )


    def _post_unpack( self, items ):
        items = super(_ArchiveBStruct,self)._post_unpack( items )
        items['LeafTemps']   = tuple(
                t-90 for t in struct.unpack('2B',items['LeafTemps']))
        items['LeafWetness'] = struct.unpack('2B',items['LeafWetness'])
        items['ExtraTemps'] = tuple(
                t-90 for t in struct.unpack('3B',items['ExtraTemps']))
        return items

# --------------------------------------------------------------------------- #

# simple data structures
DmpStruct = Struct(
        (('Pages','H'),('Offset','H'),('CRC','H')),
        order='=')

DmpPageStruct = Struct(
        (('Index','B'),('Records','260s'),('unused','4B'),('CRC','H')),
        order='=')

# init structure classes
LoopStruct      = LoopStruct()
ArchiveAStruct  = _ArchiveAStruct()
ArchiveBStruct  = _ArchiveBStruct()


##############################################################################
#|--------------------------------------------------------------------------|#
#|--------------------------------------------------------------------------|#
#|                     API for the Davis Vantage Pro                        |#
#|--------------------------------------------------------------------------|#
#|--------------------------------------------------------------------------|#
##############################################################################

class VantagePro(object):
    '''
    A class capable of reading raw (binary) weather data from a
    vantage pro console and parsing it into usable scalar
    (integer/long/real) values.

    The data read from the console is in binary format. The data is in
    least-ordered nybble strategy, and must be read with correct sizes and
    offsets for proper byte ordering.
    '''

    # device reply commands
    WAKE_ACK = '\n\r'
    ACK      = '\x06'
    ESC      = '\x1b'
    OK       = '\n\rOK\n\r'

    # archive format type, unknown
    _ARCHIVE_REV_B = None

    def __init__(self, device, log_interval=5):
        self.port = serial.Serial(device, BAUD, timeout=READ_DELAY)
        self._archive_time  = (0,0)
        # clear archive, and set loggin interval
        self._cmd('CLRLOG')     # prevent getting a full log dump at startup
        self._cmd('SETPER', log_interval, ok=True)


    def __del__(self):
        '''
        close serial port when object is deleted.
        '''
        self.port.close()


    def _use_rev_b_archive(self,records,offset):
        '''
        return True if weather station returns Rev.B archives
        '''
        # if pre-determined, return result
        if type(self._ARCHIVE_REV_B) is bool:
            return self._ARCHIVE_REV_B
        # assume, B and check 'RecType' field
        data = ArchiveBStruct.unpack_from( records, offset )
        if data['RecType'] == 0:
            log.info('detected archive rev. B')
            self._ARCHIVE_REV_B = True
        else:
            log.info('detected archive rev. A')
            self._ARCHIVE_REV_B = False

        return self._ARCHIVE_REV_B


    def _wakeup(self):
        '''
        issue wakeup command to device to take out of standby mode.
        '''
        log.info("send: WAKEUP")
        for i in xrange(3):
            self.port.write('\n')                    # wakeup device
            ack = self.port.read(len(self.WAKE_ACK)) # read wakeup string
            log_raw('read',ack)
            if ack == self.WAKE_ACK:
                return
        raise NoDeviceException('Can not access weather station')


    def _cmd(self,cmd,*args,**kw):
        '''
        write a single command, with variable number of arguments. after the
        command, the device must return ACK
        '''
        ok = kw.setdefault('ok',False)

        self._wakeup()
        if args:
            cmd = "%s %s" % (cmd, ' '.join(str(a) for a in args))
        for i in xrange(3):
            log.info("send: " + cmd)
            self.port.write( cmd + '\n')
            if ok:
                ack = self.port.read(len(self.OK))  # read OK
                log_raw('read',ack)
                if ack == self.OK:
                    return
            else:
                ack = self.port.read(len(self.ACK))  # read ACK
                log_raw('read',ack)
                if ack == self.ACK:
                    return
        raise NoDeviceException('Can not access weather station')


    def _loop_cmd(self):
        '''
        reads a raw string containing data read from the device
        provided (in /dev/XXX) format. all reads are non-blocking.
        '''
        self._cmd( 'LOOP', 1 )
        raw = self.port.read( LoopStruct.size ) # read data
        log_raw('read',raw)
        return raw


    def _dmpaft_cmd(self, time_fields):
        '''
        issue a command to read the archive records after a known time stamp.
        '''
        records = []
        # convert time stamp fields to buffer
        tbuf = struct.pack('2H',*time_fields)

        # 1. send 'DMPAFT' cmd
        self._cmd('DMPAFT')

        # 2. send time stamp + crc
        crc = VProCRC.get( tbuf )
        crc = struct.pack('>H',crc)             # crc in big-endian format
        log_raw('send', tbuf + crc)
        self.port.write( tbuf + crc )           # send time stamp + crc
        ack = self.port.read(len(self.ACK))     # read ACK
        log_raw('read',ack)
        if ack != self.ACK: return              # if bad ack, return

        # 3. read pre-amble data
        raw = self.port.read( DmpStruct.size )
        log_raw('read',raw)
        if not VProCRC.verify( raw ):           # check CRC value
            log_raw('send ESC',self.ESC)
            self.port.write( self.ESC )         # if bad, escape and abort
            return
        log_raw('send ACK',self.ACK)
        self.port.write( self.ACK )             # send ACK

        # 4. loop through all page records
        dmp = DmpStruct.unpack(raw)
        log.info( 'reading %d pages, start offset %d' %
                (dmp['Pages'],dmp['Offset']))
        for i in xrange(dmp['Pages']):
            # 5. read page data
            raw = self.port.read( DmpPageStruct.size )
            log_raw('read',raw)
            if not VProCRC.verify( raw ):       # check CRC value
                log_raw('send ESC',self.ESC)
                self.port.write( self.ESC )     # if bad, escape and abort
                return
            log_raw('send ACK',self.ACK)
            self.port.write( self.ACK )         # send ACK

            # 6. loop through archive records
            page = DmpPageStruct.unpack(raw)
            offset = 0  # assume offset at 0
            if i == 0:
                offset = dmp['Offset'] * ArchiveAStruct.size
            while offset < ArchiveAStruct.size * 5:
                log.info( 'page %d, reading record at offset %d' %
                        (page['Index'],offset))
                if self._use_rev_b_archive( page['Records'], offset ):
                    a = ArchiveBStruct.unpack_from( page['Records'], offset )
                else:
                    a = ArchiveAStruct.unpack_from( page['Records'], offset )
                # 7. verify that record has valid data, and store
                if a['DateStamp'] != 0xffff and a['TimeStamp'] != 0xffff:
                    records.append( a )
                offset += ArchiveAStruct.size
        log.info('read all pages')
        return records


    def _get_loop_fields(self):
        for i in xrange(3):
            raw = self._loop_cmd()  # read raw data
            crc_ok = VProCRC.verify( raw )
            if crc_ok: break                # exit loop if valid
            time.sleep(1)

        if not crc_ok:
            raise NoDeviceException('Can not access weather station')

        return LoopStruct.unpack(raw)


    def _get_new_archive_fields(self):
        '''
        returns a dictionary of fields from the newest archive record in the
        device. return None when no records are new.
        '''
        for i in xrange(3):
            records = self._dmpaft_cmd( self._archive_time )
            if records is not None: break
            time.sleep(1)

        if records is None:
            raise NoDeviceException('Can not access weather station')

        # find the newest record
        new_rec = None
        for r in records:
            new_time = (r['DateStamp'],r['TimeStamp'])
            if self._archive_time < new_time:
                self._archive_time = new_time
                new_rec = r

        return new_rec


    def _calc_derived_fields(self, fields):
        '''
        calculates the derived fields (those fields that are calculated)
        '''
        # convenience variables for the calculations below
        temp        = fields['TempOut']
        hum         = fields['HumOut']
        wind        = fields['WindSpeed']
        wind10min   = fields['WindSpeed10Min']
        fields['HeatIndex'] = calc_heat_index(temp, hum)
        fields['WindChill'] = calc_wind_chill(temp, wind, wind10min)
        fields['DewPoint']  = calc_dewpoint(temp, hum)
        # store current data string
        now = time.localtime()
        fields['DateStamp'] = time.strftime("%Y-%m-%d %H:%M:%S", now)
        fields['Year'] = now[0]
        fields['Month'] = str(now[1]).zfill(2)
        now = time.gmtime()
        fields['DateStampUtc'] = time.strftime("%Y-%m-%d %H:%M:%S", now)
        fields['YearUtc'] = now[0]
        fields['MonthUtc'] = str(now[1]).zfill(2)


    def parse(self):
        '''
        read and parse a set of data read from the console.  after the
        data is parsed it is available in the fields variable.
        '''
        fields  = self._get_loop_fields()
        fields['Archive'] = self._get_new_archive_fields()

        self._calc_derived_fields( fields )

        # set the fields variable the the values in the dict
        self.fields = fields


# vim: sts=4:ts=4:sw=4
