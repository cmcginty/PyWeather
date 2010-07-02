#! /usr/bin/env python
#
# PyWeather
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

import os
from distutils.core import setup

import weather as pkg
name = pkg.__name__

def _read( *path_name ):
   return open( os.path.join(os.path.dirname(__file__), *path_name)).read()

setup(name = name,
      version = pkg.__version__,
      license = "GNU GPL",
      description = pkg.__doc__,
      long_description=_read('README'),
      author = "Patrick C. McGinty, Christopher Blunck",
      author_email = "pyweather@tuxcoder.com, chris@wxnet.org",
      url = "http://oss.wxnet.org/pyweather",
      download_url = "",
      packages= [
         name,
         name+'.services',
         name+'.stations',
         name+'.units',
      ],
      scripts= [ 'scripts/vpro-to-wu.py' ],
   )
