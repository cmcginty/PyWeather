'''
PWSweather.com Publisher
WeatherForYou.com Publisher

Abstract:
The class contained within this module allows python programs to
publish weather conditions to the pwsweather.com servers.

Usage:
>>> publisher = PWS( 'MySiteID', 'MyPassowrd')
>>> publisher.set( ... )
>>> response = publisher.publish()
>>> print '%s: %s' % (response.status, response.reason)

Notes on arguments to Publisher.set():
<float> pressure:   in inches of Hg
<float> dewpoint:   in Fahrenheit
<float> humidity:   between 0.0 and 100.0 inclusive
<float> tempf:      in Fahrenheit
<float> rainin:     inches/hour of rain
<float> rainday:    total rainfall for day (localtime)
<float> rainmonth:  total rainfall for month (localtime)
<float> rainyear:   total rainfall for year (localtime)
<tuple> dateutc:    9 value time tuple in UTC (e.g. time.gmtime())
<float> windgust:   in mph
<float> windspeed:  in mph
<float> winddir:    in degrees, between 0.0 and 360.0
<string> weather:   unknown at this time (email me if you know!)

Author: Patrick C. McGinty (pyweather@tuxcoder.com)
Date: Tuesday, July 13 2010
'''

from __future__ import absolute_import

import logging
log = logging.getLogger(__name__)

from . _base import *


class PWS(HttpPublisher):
   '''
   Publishes weather data to the pwsweather.com servers. See module
   documentation for additional information and usage idioms.
   '''
   STD_SERVER = "www.pwsweather.com"
   URI = "/pwsupdate/pwsupdate.php"

   def __init__(self, sid, password):
      super(PWS,self).__init__(sid,password)
      self.args = {  'ID':sid,
                     'PASSWORD':password,
                     'action':'updateraw',
                     'softwaretype':self.SOFTWARE, }
      self.server = self.STD_SERVER


   def set( self, pressure='NA', dewpoint='NA', humidity='NA', tempf='NA',
         rainin='NA', rainday='NA', rainmonth='NA', rainyear='NA',
         dateutc='NA', windgust='NA', windspeed='NA', winddir='NA',
         weather='NA', *args, **kw):
      '''
      Usefull for defining weather data published to the server. Parameters not
      sent will be cleared and not set to server. Unknown keyword args will be
      silently ignored, so be careful. This is necessory for publishers that
      support more fields than others.
      '''
      # unused, but valid, parameters are:
      #   solarradiation, UV
      self.args.update( {
            'baromin':pressure,
            'dailyrainin':rainday,
            'dateutc':dateutc,
            'dewptf':dewpoint,
            'humidity':humidity,
            'monthrainin':rainmonth,
            'rainin':rainin,
            'tempf':tempf,
            'weather':weather,
            'winddir':winddir,
            'windgustmph':windgust,
            'windspeedmph':windspeed,
            'yearrainin':rainyear,
          } )
      log.debug( self.args )


   def publish( self, *a, **kw):
      http = super( PWS, self).publish( *a, **kw)
      if not http[2].find('Logged and posted') >= 0:
         raise PublishException('Server returned invalid status: %d %s %s'
              % http)
      return http

