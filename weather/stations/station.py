'''Base class for all Weather Station implementations.'''

from dataclasses import dataclass

import datetime

__all__ = ['WeatherPoint', 'Station']


@dataclass
class WeatherPoint:
    '''Data class representing a single weather measurement.'''
    time: datetime.datetime

    temperature_f: float  # Temperature in Fahrenheit
    humidity: int  # Relative humidity in percent
    dew_point_f: float  # Dew point in Fahrenheit
    pressure: int = None  # Atmosperic pressure

    rain_rate_in: float = None  # Rain rate in inches
    rain_day_in: float = None  # Rain inches so far today

    wind_speed_mph: float = None  # Wind speed in miles per hour
    wind_direction: int = None  # Wind direction, in degrees


class Station:
    '''Base class for all Weather Station implementations.'''

    def get_reading() -> WeatherPoint:
        '''Returns a single weather point.'''
        raise NotImplementedError('Not implemented')
