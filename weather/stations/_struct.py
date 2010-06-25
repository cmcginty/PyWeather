'''
Binary Data Interfaces

Abstract:
Helper classes for working with binary data structures. This simplifies data
field extraction from a binary buffer.

Author: Patrick C. McGinty (pyweather@tuxcoder.com)
Date: 2010-06-025
'''

from __future__ import absolute_import

import struct


class Struct( struct.Struct ):
    '''
    Implements a reusable class for working with a binary data structure. It
    provides a named fields interface, similiar to C structures.

    Usage: 1) subclass and extend _post_unpack method
           2) instantiate directly, if no 'post unpack' processing needed

    Arguments:
        See `struct.Struct` class defintion.
    '''
    def __init__(self, fmt, order='@'):
        self.fields, fmt_t = zip(*fmt)
        super(Struct,self).__init__( order + ''.join(fmt_t) )


    def unpack(self, buf):
        '''
        see unpack_from()
        '''
        return self.unpack_from( buf, offset=0 )


    def unpack_from(self, buf, offset=0 ):
        '''
        unpacks data from 'buf' and returns a dication of named fields. the
        fields can be post-processed by extending the _post_unpack() method.
        '''
        data = super(Struct,self).unpack_from( buf, offset)
        items = dict(zip(self.fields,data))
        return self._post_unpack(items)


    def _post_unpack(self,items):
        '''
        perform data modification of any values, after unpacking from a buffer.
        '''
        return items

# vim: sts=4:ts=4:sw=4
