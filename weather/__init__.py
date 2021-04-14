'''
PyWeather branch; bindings for Davis Vantage Pro and Pro2 weather stations,
upload of weather data (e.g. wunderground.com), and meteorological
calculation/conversion functions.
'''

__version__ = '0.11.0'

import logging


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


# init a null handler, to prevent warnings
logging.getLogger(__name__).addHandler(NullHandler())
