#!/usr/bin/env python

#
# See __usage__ for an explanation of runtime arguments.
#
# -Christopher Blunck
#

import sys, time

__author__ = 'Christopher Blunck'
__email__ = 'chris@wxnet.org'
__revision__ = '$Revision: 1.6 $'

__doc__ = '''
Demonstrates how to call the wunderground publisher.  See the
wunderground module for more information.
'''

__usage__ = '''
  python $0
'''


def usage():
    print __usage__
    sys.exit(1)


def wunderground():
    # wunderground.com username and password
    USERNAME = "KMDCOLLE3"
    PASSWORD = "blah99"

    # call the real time server by passing a rtfreq parameter
    from wunderground import Publisher
    publisher = Publisher(10.0)
    
    # set the current conditions
    publisher.set(30.18, 24.84, 48.00, 43.30, 
                  0.0, time.gmtime(), 0.0, 0.0, 0.0)
    
    # publish to the server
    response = publisher.publish(WUNDERGROUND_USERNAME, WUNDERGROUND_PASSWORD)

    # the response (always OK)
    print '%s: %s' % (response.status, response.reason)



def main():
    wunderground()


if __name__ == '__main__':
    main()
