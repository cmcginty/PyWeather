#! /usr/bin/env python
#
# pyweather
# (c) 2005 Christopher Blunck <chris@wxnet.org>
#
# You're welcome to redistribute this software under the
# terms of the GNU General Public Licence version 2.0
# or, at your option, any higher version.
#
# You can read the complete GNU GPL in the file COPYING
# which should come along with this software, or visit
# the Free Software Foundation's WEB site http://www.fsf.org
#
# $Id: $

from distutils.core import setup

import weather

setup(name = "weather",
      version = weather.__version__,
      license = "GNU GPL",
      description = weather.__doc__,
      author = "Christopher Blunck",
      author_email = "chris@wxnet.org",
      url = "http://oss.wxnet.org/pyweather",
      packages= [ "weather", "weather.units", "weather.stations", "weather.services" ])
