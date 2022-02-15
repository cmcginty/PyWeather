"""Base class for all Weather Station implementations."""

import datetime
import time as time_module

from ..units.temp import fahrenheit_to_celsius, celsius_to_fahrenheit

__all__ = ['WeatherPoint', 'Station']


class WeatherPoint:
    """
    Represents a single weather measurement.
    """
    time: datetime.datetime = None

    _temperature_c: float = None  # Temperature in Celsius
    _temperature_f: float = None  # Temperature in Fahrenheit
    humidity: int = None  # Relative humidity in percent
    dew_point_f: float = None  # Dew point in Fahrenheit
    pressure: float = None  # Atmospheric pressure

    rain_rate_in: float = None  # Rain rate in inches
    rain_day_in: float = None  # Rain inches so far today

    wind_speed_mph: float = None  # Wind's speed in miles per hour
    wind_direction: int = None  # Wind's direction, in degrees

    def __init__(
            self,
            time=None,
            temperature_c: float = None,
            temperature_f: float = None,
            humidity: int = None,
            dew_point_f: float = None,
            pressure: float = None,
            rain_rate_in: float = None,
            rain_day_in: float = None,
            wind_speed_mph: float = None,
            wind_direction: int = None,
            ):
        self.time = time or time_module.gmtime()
        if temperature_c is not None and temperature_f is not None:
            raise ValueError('Only one of temperature_c and temperature_f can be passed.')
        if temperature_c is not None:
            self.temperature_c = temperature_c
        else:
            self.temperature_f = temperature_f
        self.humidity = humidity
        self.dew_point_f = dew_point_f
        self.pressure = pressure
        self.rain_rate_in = rain_rate_in
        self.rain_day_in = rain_day_in
        self.wind_speed_mph = wind_speed_mph
        self.wind_direction = wind_direction

    @property
    def temperature_f(self) -> float:
        if self._temperature_f is not None:
            return self._temperature_f
        elif self._temperature_c is not None:
            return celsius_to_fahrenheit(self._temperature_c)

    @temperature_f.setter
    def temperature_f(self, value: float):
        self._temperature_f = value
        self._temperature_c = None

    @property
    def temperature_c(self) -> float:
        if self._temperature_c is not None:
            return self._temperature_c
        elif self._temperature_f is not None:
            return fahrenheit_to_celsius(self._temperature_f)

    @temperature_c.setter
    def temperature_c(self, value: float):
        self._temperature_f = None
        self._temperature_c = value

    def __eq__(self, other):
        return (
            self.time == other.time and
            self._temperature_c == other._temperature_c and
            self._temperature_f == other._temperature_f and
            self.humidity == other.humidity and
            self.dew_point_f == other.dew_point_f and
            self.pressure == other.pressure and
            self.rain_rate_in == other.rain_rate_in and
            self.rain_day_in == other.rain_day_in and
            self.wind_speed_mph == other.wind_speed_mph and
            self.wind_direction == other.wind_direction
        )

    def __repr__(self):
        return str(self.__dict__)


class Station:
    """Base class for all Weather Station implementations."""

    def get_reading(self) -> WeatherPoint:
        """Returns a single weather point."""
        raise NotImplementedError('Not implemented')
