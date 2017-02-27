'''
This module shows how to use the vantage_weatherLinkIP module

Author: Paolo Bellagente - University of Brescia
Date: 2017-02-24
'''

from weather.stations.davis_weatherLinkIP import *
import datetime as dt
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, filename="davisip.log")


if __name__ == '__main__':
    # Console IP
    IP = "xxx.xxx.xxx.xxx"

    # Davis default port
    PORT = 22222

    console = VantagePro(IP,PORT)
    logging.debug("archiveTime: "+str(console._archive_time))
    print "Connect to Console "+IP+" on port "+str(PORT)
    # set the archive time to 10 min ago
    ts = dt.datetime.now() - dt.timedelta(minutes=10)
    print "Get records from "+str(ts.year)+"/"+str(ts.month)+"/"+str(ts.day)+" "+str(ts.hour)+":"+str(ts.minute)
    console.setArchiveTime(ts)
    logging.debug("archiveTime: " + str(console._archive_time))
    console.parse()
    print console.fields