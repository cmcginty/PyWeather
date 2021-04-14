'''
Common base classes for PyWeather pulication services.
'''


import logging
log = logging.getLogger(__name__)


class PublishException(Exception):
    pass


class HttpPublisher(object):
    '''
    Abstract base class for creation generic HTTP publication services
    '''
    SOFTWARE = 'PyWeather'
    STD_SERVER = None
    REALTIME_SERVER = None
    URI = None

    def __init__(self, sid, password, rtfreq=None):
        self.sid = sid
        self.password = password
        self.rtfreq = rtfreq

    def set(self, *args, **kw):
        '''
        Useful for defining weather data published to the server. Each
        publication service implements their own supported keyword args, but
        should support any number of arguments.
        '''
        raise NotImplementedError("abstract method")

    @staticmethod
    def _publish(args, server, uri):
        from http.client import HTTPConnection, HTTPSConnection
        from urllib.parse import urlencode

        args = {k: v for k, v in args.items() if v is not None and v != 'NA'}
        uri = uri + "?" + urlencode(args)

        log.debug('Connect to: https://%s' % server)
        log.debug('GET %s' % uri)

        conn = HTTPSConnection(server, timeout=5)
        if not conn:
            raise PublishException('Remote server connection timeout')
        conn.request("GET", uri)

        http = conn.getresponse()
        data = (http.status, http.reason, http.read())
        conn.close()
        if not (data[0] == 200 and data[1] == 'OK'):
            raise PublishException(
                'Server returned invalid status: %d %s %s' % data)
        return data

    def publish(self):
        '''
        Perform HTTP session to transmit defined weather values.
        '''
        return self._publish(self.args, self.server, self.URI)
