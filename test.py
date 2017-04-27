'''
This module shows how to use the vantage_weatherLinkIP module

Author: Paolo Bellagente - University of Brescia
Date: 2017-02-24
'''

from weather.stations.davis_weatherLinkIP import *
import datetime as dt
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR
                    , filename="davisip.log"
                    )


if __name__ == '__main__':
    # Console IP
    IP = "x.x.x.x"
    # Davis default port
    PORT = 22222
    # Console logging interval in minutes Valid values are (1, 5, 10, 15, 30, 60, and 120). Results are undefined if you try to select an archive period not on the list.
    ARCHIVE_INTERVAL = 1
    console = VantagePro(IP,PORT, ARCHIVE_INTERVAL)
    logging.debug("archiveTime: "+str(console._archive_time))
    print "Connect to Console "+IP+" on port "+str(PORT)
    # set the archive time to 10 min ago
    ts = dt.datetime.now() - dt.timedelta(minutes=5)
    print "Get records from "+str(ts.year)+"/"+str(ts.month)+"/"+str(ts.day)+" "+str(ts.hour)+":"+str(ts.minute)
    console.setArchiveTime(ts)
    logging.debug("archiveTime: " + str(console._archive_time))
    console.parse()
    print len(console.fields)
    print console.fields