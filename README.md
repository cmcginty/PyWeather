# PyWeather

## Abstract

PyWeather contains weather related modules implemented in Python.
Anything weather related is fair game for PyWeather.  Currently
PyWeather is limited to unit conversion, console reading, and data
publication.  But, future work can be added to PyWeather in any area.


## Unit Conversion

PyWeather has a lot of support for common unit conversions in
distance, temperature, pressure, and volume.  Conversion from
Fahrenheit to Celsius, and kelvin is supported, as well as conversions
between inches of mercury and millibars.


## Station Observations

PyWeather also contains modules that are capable of downloading
observations from weather consoles.  The current list of supported
weather consoles includes:

-   Davis Vantage Pro
-   Davis Vantage Pro2
-   Netatmo weather station.


## Data Publication

PyWeather contains a module that allows developers to post conditions
to weather aggregation sites. The current list of support services includes:

-   WeatherUnderground (wundgerground.com)
-   PWS Weather        (pwsweather.com)
-   WeatherForYou      (weatherforyou.com)


For additional information, please email the maintainer:
   pyweather@tuxcoder.com

## Data Publication Script

`scripts/weatherpub.py` supports publication of the weather data. It can also serve as a good usage example.

### General usage

1.  Copy `weatherpub.conf.example` as `weatehrpub.conf`.
2.  Modify `weatehrpub.conf`:
3.  In `[general]` section set `station` to the name of the station you have.
4.  Set `publication` to a comma-separated list of weather services you'd like
    to push data to.
5.  Configure weather station and publication service in corresponding sections
    of the configuration file (see below for more details).
3.  Run it: `./scripts/weatherpub.py -c scripts/weatherpub.conf`

### Weather stations

The script supports Vantage Pro and Netatmo. Vantage Pro support was not recently tested and may be broken by the latest update. Please report bugs and/or send pull requests.

#### Vantage Pro

By default script excepts Vantage Pro weather stations to be connected to /`/dev/ttyS0`. Use `--tty` command-line flag to override it (this cannot be currently set via command-line), e.g. `./scripts/weatherpub.py -c scripts/weatherpub.conf --tty /dev/ttyS1`

#### Netatmo

Since netatmo works via public API, some setup required first:

1.  [Create a Netatmo app](https://dev.netatmo.com/apps/createanapp#form).
2.  Use generated app id and secret as `client_id` and `client_secret`.
3.  Use your own Netatmo username (e-mail) as `username` and `password`.
4.  Set `module_name` to your outdoor module name, e.g. 'Outdoor'.

Note: Rain Gauge and Anemometer are not supported yet.

### Publication services

Only 3 publication service are currently supported. Out of them only PWS Weather was properly tested.

#### PWS Weather

1.  [Create PWS Weather profile](https://www.pwsweather.com/register).
2.  Go to your [dashboard](https://dashboard.pwsweather.com/) and [create a station](https://dashboard.pwsweather.com/stations/add).
3.  In `[pwsweather]` section of the configuration file use your station id as `site_id`, and password from account you created at step 1 as `password`.
