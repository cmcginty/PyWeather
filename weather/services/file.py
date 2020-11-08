'''
Local File Publisher

Abstract:
The class contained within this module allows python programs to
publish weather conditions to a local text file. The format of the file is:

   field value [value ...]
   field value [value ...]
   field value [value ...]
   ...
   ...

Each 'field' will begin on a separate line. The 'field' parameter is always a
single word. Depending on the field, there maybe be multiple 'value'
parameters. All fields and values are separated by a single space. String
values will be surrounded by quotes.

This class does not define field names. The implementation assigns field names
from the keyword parameters passed to it through the set() method. Therefore it
is up to the user to define all field names using named parameters with the
'set()' method. If you desire to keep the TextFile.set() command compatible
with other set() publisher methods, please reference the other classes for
expected field names.

Usage:
>>> publisher = TextFile( 'file_name' )
>>> publisher.set( ... )
>>> publisher.publish()

Author: Patrick C. McGinty (pyweather@tuxcoder.com)
Date: Thursday, July 15 2010
'''



import io
import logging
log = logging.getLogger(__name__)

from . _base import *


class TextFile(object):
   '''
   Publishes weather data to a local file. See module
   documentation for additional information and usage idioms.
   '''
   def __init__(self, file_name):
      self.file_name = file_name
      self.args = {}

   def set( self, **kw):
      '''
      Store keyword args to be written to output file.
      '''
      self.args = kw
      log.debug( self.args )


   @staticmethod
   def _append_vals( buf, val):
      if isinstance(val,dict):
         msg = 'unsupported %s type: %s' % (type(val),repr(val),)
         log.error(msg)
      if isinstance(val,(list,tuple)):
         for i in val:
           TextFile._append_vals(buf, i)
      else:
         buf.write(' ' + repr(val))


   def publish(self):
      '''
      Write output file.
      '''
      with open( self.file_name, 'w') as fh:
         for k,v in self.args.items():
            buf = io.StringIO()
            buf.write(k)
            self._append_vals(buf,v)
            fh.write(buf.getvalue() + '\n')
            buf.close() # free string buffer



