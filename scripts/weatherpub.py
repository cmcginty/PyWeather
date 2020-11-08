#!/usr/bin/env python
#
#  PyWeather example script for reading PyWeather stations uploading to one or
#  more PyWeather publication sites
#
#  Author:  Patrick C. McGinty
#  Email:   pyweather@tuxcoder.com
#  Date:    Sunday, May 02 2010
'''
Periodically read data from a local weather station and upload to the PyWeather
publication site.
'''

import os
import sys
import time
import logging
import optparse

import weather.stations
import weather.services

log = logging.getLogger('')

ARCHIVE_INTERVAL  = 10  # intervals (in minutes) between each archive record
                        # generated by the weather station
GUST_TTL          = 10  # gust 'time to live'; define many minutes should
                        # gust be reported
GUST_MPH_MIN      = 7   # minimum mph of gust above avg wind speed to report

# Publication Services Lookup Table
#     key expected to match optparse destination parameter
#     value defines class object of publication service
PUB_SERVICES = {
      'wug'    : weather.services.Wunderground,
      'pws'    : weather.services.PwsWeather,
      'file'   : weather.services.TextFile,
   }


class NoSensorException(Exception): pass


class WindGust(object):
   NO_VALUE = ('NA','NA')

   def __init__(self):
      self.value = self.NO_VALUE
      self.count = 0

   def get( self, station, interval ):
      '''
      return gust data, if above threshold value and current time is inside
      reporting window period
      '''
      rec = station.fields['Archive']
      # process new data
      if rec:
         threshold = station.fields['WindSpeed10Min'] + GUST_MPH_MIN
         if rec['WindHi'] >= threshold:
            self.value = (rec['WindHi'],rec['WindHiDir'])
            self.count = GUST_TTL * 60 / interval
         else:
            self.value = self.NO_VALUE

      # return gust value, if remaining time is left, and valid
      if self.count:
         self.count -= 1
      else:
         self.value = self.NO_VALUE

      log.debug('wind gust of {0} mph from {1}'.format(*self.value))
      return self.value
WindGust = WindGust()


def weather_update(station, pub_sites, interval):
   '''
   main execution loop. query weather data and post to online service.
   '''
   station.parse()      # read weather data

   # santity check weather data
   if station.fields['TempOut'] > 200:
      raise NoSensorException(
            'Out of range temperature value: %.1f, check sensors' %
            (station.fields['TempOut'],))

   gust, gust_dir = WindGust.get( station, interval )

   # upload data in the following order:
   for ps in pub_sites:
      try: # try block necessary to attempt every publisher
         ps.set(
               pressure    = station.fields['Pressure'],
               dewpoint    = station.fields['DewPoint'],
               humidity    = station.fields['HumOut'],
               tempf       = station.fields['TempOut'],
               rainin      = station.fields['RainRate'],
               rainday     = station.fields['RainDay'],
               dateutc     = station.fields['DateStampUtc'],
               windspeed   = station.fields['WindSpeed10Min'],
               winddir     = station.fields['WindDir'],
               windgust    = gust,
               windgustdir = gust_dir, )

         ps.publish()
      except (Exception) as e:
         log.warn('publisher %s: %s'%(ps.__class__.__name__,e))


def init_log( quiet, debug ):
   '''
   setup system logging to desired verbosity.
   '''
   from logging.handlers import SysLogHandler
   fmt = logging.Formatter( os.path.basename(sys.argv[0]) +
         ".%(name)s %(levelname)s - %(message)s")
   facility = SysLogHandler.LOG_DAEMON
   syslog = SysLogHandler(address='/dev/log',facility=facility)
   syslog.setFormatter( fmt )
   log.addHandler(syslog)
   if not quiet:
      console = logging.StreamHandler()
      console.setFormatter( fmt )
      log.addHandler(console)
      log.setLevel(logging.INFO)
      if debug:
         log.setLevel(logging.DEBUG)


def get_pub_services(opts):
   '''
   use values in opts data to generate instances of publication services.
   '''
   sites = []
   for p_key in list(vars(opts).keys()):
      args = getattr(opts,p_key)
      if p_key in PUB_SERVICES and args:
         if isinstance(args,tuple):
            ps = PUB_SERVICES[p_key](*args)
         else:
            ps = PUB_SERVICES[p_key](args)
         sites.append( ps )
   return sites


def get_options(parser):
   '''
   read command line options to configure program behavior.
   '''
   # station services
   # publication services
   pub_g = optparse.OptionGroup( parser, "Publication Services",
         '''One or more publication service must be specified to enable upload
         of weather data.''', )
   pub_g.add_option('-w', '--wundergound', nargs=2, type='string', dest='wug',
         help='Weather Underground service; WUG=[SID(station ID), PASSWORD]')
   pub_g.add_option('-p', '--pws', nargs=2, type='string', dest='pws',
         help='PWS service; PWS=[SID(station ID), PASSWORD]')
   pub_g.add_option('-f', '--file', nargs=1, type='string', dest='file',
         help='Local file; FILE=[FILE_NAME]')
   parser.add_option_group(pub_g)

   parser.add_option('-d', '--debug', dest='debug', action="store_true",
         default=False, help='enable verbose debug logging')
   parser.add_option('-q', '--quiet', dest='quiet', action="store_true",
         default=False, help='disable all console logging')
   parser.add_option('-t', '--tty', dest='tty', default='/dev/ttyS0',
         help='set serial port device [/dev/ttyS0]')
   parser.add_option('-n', '--interval', dest='interval', default=60,
         type='int', help='polling/update interval in seconds [60]')
   return parser.parse_args()


if __name__ == '__main__':
   parser = optparse.OptionParser()
   opts,args = get_options(parser)
   init_log( opts.quiet, opts.debug )

   # configure publication service defined in command-line args
   pub_sites = get_pub_services(opts)

   if not pub_sites:
      log.error('no publication service defined')
      sys.exit(-1)

   station = weather.stations.VantagePro(opts.tty, ARCHIVE_INTERVAL)

   while True:
      # pause until next update time
      next_update = opts.interval - (time.time() % opts.interval)
      log.info('sleep')
      time.sleep( next_update )

      try:
         weather_update( station, pub_sites, opts.interval)
      except (Exception) as e:
         log.error(e)

