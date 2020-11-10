'''
WUnderground.com Publisher

Abstract:
The class contained within this module allows python programs to
publish weather conditions to the wunderground.com servers.  That is,
this class encapsulates the wire protocol wunderground.com supports
and allows application developers to insulate themselves against
changes in the wunderground.com wire protocol.

If the rtfreq parameter is passed to the Publisher constructor,
posting of the current conditions will go to the "real time updater"
service provided by wunderground.com.  The rtfreq optional parameter
passed to the constructor is a float that represents the number of
seconds between observations.

Usage:
>>> publisher = Wunderground( 'MySiteID', 'MyPassowrd')
>>> publisher.set( ... )
>>> response = publisher.publish()
>>> print '%s: %s' % (response.status, response.reason)

Notes on arguments to Publisher.set():
<float> pressure:   in inches of Hg
<float> dewpoint:   in Fahrenheit
<float> humidity:   between 0.0 and 100.0 inclusive
<float> tempf:      in Fahrenheit
<float> rainin:     inches/hour of rain
<float> rainday:    total rainfall in day (localtime)
<string> dateutc:   date "YYYY-MM-DD HH:MM:SS" in GMT timezone
<float> windgust:   in mph
<float> windgustdir:in degrees, between 0.0 and 360.0
<float> windspeed:  in mph
<float> winddir:    in degrees, between 0.0 and 360.0
<string> clouds:    unknown at this time (email me if you know!)
<string> weather:   unknown at this time (email me if you know!)

Developers Notes:
It appears that even if you provide an invalid username and password,
a status of 200, and a reason of "OK" is returned.

Author: Patrick C. McGinty (pyweather@tuxcoder.com)
Date: Tuesday, July 13 2010
Author: Christopher Blunck (chris@wxnet.org)
Date: 2006-03-27
'''


import logging

from . _base import *

log = logging.getLogger(__name__)


class Wunderground(HttpPublisher):
    '''
    Publishes weather data to the wunderground.com servers.  See
    module documentation for additional information and usage idioms.
    '''
    STD_SERVER = "weatherstation.wunderground.com"
    REALTIME_SERVER = "rtupdate.wunderground.com"
    URI = "/weatherstation/updateweatherstation.php"

    def __init__(self, sid, password, rtfreq=None):
        super(Wunderground, self).__init__(sid, password)
        self.args = {'ID': sid,
                     'PASSWORD': password,
                     'action': 'updateraw',
                     'softwaretype': self.SOFTWARE, }
        if rtfreq:
            self.args['realtime'] = 1
            self.args['rtfreq'] = self.rtfreq
            self.server = self.REALTIME_SERVER
        else:
            self.server = self.STD_SERVER

    def set(self, pressure='NA', dewpoint='NA', humidity='NA', tempf='NA',
            rainin='NA', rainday='NA', dateutc='NA', windgust='NA',
            windgustdir='NA', windspeed='NA', winddir='NA',
            clouds='NA', weather='NA', *args, **kw):
        '''
        Useful for defining weather data published to the server. Parameters
        not set will be reset and not sent to server. Unknown keyword args will
        be silently ignored, so be careful. This is necessary for publishers
        that support more fields than others.
        '''
        # see: http://wiki.wunderground.com/index.php/PWS_-_Upload_Protocol
        # unused, but valid, parameters are:
        #   windspdmph_avg2m, winddir_avg2m, windgustmph_10m, windgusdir_10m
        #   soiltempf, soilmoisture, leafwetness, solarradiation, UV
        #   indoortempf, indoorhumidity
        self.args.update({
                'baromin': pressure,
                'clouds': clouds,
                'dailyrainin': rainday,
                'dateutc': dateutc,
                'dewptf': dewpoint,
                'humidity': humidity,
                'rainin': rainin,
                'tempf': tempf,
                'weather': weather,
                'winddir': winddir,
                'windgustdir': windgustdir,
                'windgustmph': windgust,
                'windspeedmph': windspeed,
            })
        log.debug(self.args)

    def publish(self):
        http = super(Wunderground, self).publish()
        if not http[2].find(b'success') >= 0:
            raise PublishException(
                'Server returned invalid status: %d %s %s' % http)
        return http


# for legacy support <= v0.8.2, depreciated, do not use
Publisher = Wunderground

# vim: sts=4:ts=4:sw=4
