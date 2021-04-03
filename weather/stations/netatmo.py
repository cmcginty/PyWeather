'''Netatmo Weather Station support.

https://www.netatmo.com/en-eu/weather/weatherstation

Prep:

1.  [Create a Netatmo app](https://dev.netatmo.com/apps/createanapp#form).
2.  Use generated app id and secret as `client_id` and `client_secret`.
3.  Use your own Netatmo username (e-mail) as `username` and `password`.

Example usage:

station = NetatmoStation(cliend_id='deadbeef1234567890abcdef',
                         client_secret='123',
                         username='me@example.com',
                         password='correcthorse')

pprint.pprint(station.get_reading())
'''

import datetime

from weather.stations.station import *

import pyatmo


class NetatmoStation(Station):
    '''Netatmo Weather Station support.

    Implementes as a relatively thin wrapper on top of pyatmo.
    '''

    def __init__(self, client_id: str, client_secret: str, username: str,
                 password: str, module_name: str = 'Outdoor', **kwargs):
        '''Initialize and auth Netatmo Weatehr station reader.

        See module docstring for agrs explanation.
        '''
        if kwargs:
            raise ValueError("Unknown params: %s" % ",".join(kwargs.keys()))
        self.module_name = module_name
        self._auth = pyatmo.ClientAuth(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password)

    def get_reading(self) -> WeatherPoint:
        '''Return single weather reading.

        Currently only assumes account only has one Netatmo station with
        one module. Does not support anemometer or rain gauge.
        '''
        weatherData = pyatmo.WeatherStationData(self._auth)
        # We assume there is only one station in the account.
        station_id = next(iter(weatherData.stations.values()))['_id']
        module_id = None
        for module in weatherData.get_modules(station_id).values():
            if module['module_name'] == self.module_name:
                module_id = module['id']
                break
        if module_id is None:
            raise ValueError(
                'Module %s not found, found %s' % (
                    self.module_name,
                    weatherData.get_module_names(station_id)))

        module_data = weatherData.get_module(module_id)

        return WeatherPoint(
            temperature_c=module_data['dashboard_data']['Temperature'],
            humidity=module_data['dashboard_data']['Humidity'],
            time=datetime.datetime.fromtimestamp(module_data['last_message']))
