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
>>> publisher = Publisher()
>>> publisher.set(30.12, 28.52, 53.0, 44.6, 0.0, time.gmtime(), 0, 0, 0)
>>> response = publisher.publish('MyUserName', 'MyPassword')
>>> print '%s: %s' % (response.status, response.reason)

Notes on arguments to Publisher.set():
<float> pressure:  in inches of Hg
<float> dewpt: in Fahrenheit
<float> humidity: between 0.0 and 100.0 inclusive
<float> tempf: in Fahrenheit
<time tuple> dateutc: 9 value time tuple in UTC (e.g. time.gmtime())
<float> windgust: in mph
<float> winddir: in degrees, between 0.0 and 100.0
<string> clouds: unknown at this time (email me if you know!)
<string> weather: unknown at this time (email me if you know!)

Developers Notes:
It appears that even if you provide an invalid username and password,
a status of 200, and a reason of "OK" is returned.

Author: Christopher Blunck (chris@wxnet.org)
Date: 2006-03-27
'''

from __future__ import absolute_import

import logging
log = logging.getLogger(__name__)


class PublishException(Exception): pass


class Publisher:
    '''
    Publishes weather data to the wunderground.com servers.  See
    module documentation for additional information and usage idioms.
    '''

    STD_SERVER = "weatherstation.wunderground.com"
    REALTIME_SERVER = "rtupdate.wunderground.com"
    URI = "/weatherstation/updateweatherstation.php"

    def __init__(self, rtfreq=None):
        self.args = {}
        self.rtfreq = rtfreq

    def set(self, pressure='NA', dewpoint='NA', humidity='NA', tempf='NA',
            rainin='NA', rainday='NA', dateutc='NA', windgust='NA',
            windgustdir='NA', windspeed='NA', winddir='NA',
            clouds='NA', weather='NA'):

        self.args['baromin'] = pressure
        self.args['dewptf'] = dewpoint
        self.args['humidity'] = humidity
        self.args['tempf'] = tempf
        self.args['rainin'] = rainin
        self.args['dailyrainin'] = rainday
        self.args['dateutc'] = dateutc
        self.args['windgustmph'] = windgust
        self.args['windgustdir'] = windgustdir
        self.args['windspeedmph'] = windspeed
        self.args['winddir'] = winddir
        self.args['clouds'] = clouds
        self.args['weather'] = weather
        self.args = dict((k,v) for k,v in self.args.items() if v != 'NA')
        log.debug( self.args )

    def _publish(self, user, passwd, args, server, uri, debug):
        from httplib import HTTPConnection
        from urllib import urlencode

        uri = uri + "?" + urlencode(args)

        if debug:
            print 'Connect to: http://%s' % server
            print 'GET %s' % uri
            print '\nFull URL: http://%s%s' % (server, uri)

        conn = HTTPConnection(server, timeout=5)
        if not conn:
            raise PublishException('Remote server connection timeout')
        conn.request("GET", uri)

        http = conn.getresponse()
        data = (http.status, http.reason, http.read())
        conn.close()
        if not (data[0] == 200 and
                data[1] == 'OK' and
                data[2].find('success') >= 0):
            raise PublishException('Server returned invalid status: %d %s %s'
                    % data)
        return data


    def publish(self, username, password, debug=False):
        self.args['ID'] = username
        self.args['PASSWORD'] = password
        self.args['action'] = 'updateraw'
        self.args['softwaretype'] = "PyWeather"

        server = Publisher.STD_SERVER
        if self.rtfreq:
            self.args['realtime'] = 1
            self.args['rtfreq'] = self.rtfreq
            server = Publisher.REALTIME_SERVER

        uri = Publisher.URI
        return self._publish(username, password, self.args, server, uri, debug)


# vim: sts=4:ts=4:sw=4
