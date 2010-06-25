__version__ = '0.8'

__doc__ = '''PyWeather branch; bindings for Davis Vantage Pro I/II weather
stations, upload of weather data (e.g. wunderground.com), and meteorological
calculation/conversion functions.'''

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

# init a null handler, to prevent warnings
logging.getLogger(__name__).addHandler( NullHandler() )
