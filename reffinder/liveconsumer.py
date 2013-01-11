#!/usr/bin/env python
"""
An example consumer that uses a greenlet pool to accept incoming market
messages. This example offers a high degree of concurrency.
"""
import zlib
# This can be replaced with the built-in json module, if desired.
import simplejson

import cProfile
import gevent
from gevent.pool import Pool
from gevent import monkey; gevent.monkey.patch_all()
import zmq
import scipy.stats as stats
import numpy.ma as ma
import numpy as np
from datetime import datetime
import time
import dateutil.parser

np.seterr(all='ignore')

# The maximum number of greenlet workers in the greenlet pool. This is not one
# per processor, a decent machine can support hundreds or thousands of greenlets.
# I recommend setting this to the maximum number of connections your database
# backend can accept, if you must open one connection per save op.
MAX_NUM_POOL_WORKERS = 50

def main():
    """
    The main flow of the application.
    """
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)

    # Connect to the first publicly available relay.
    subscriber.connect('tcp://relay-us-central-1.eve-emdr.com:8050')
    # Disable filtering.
    subscriber.setsockopt(zmq.SUBSCRIBE, "")

    # We use a greenlet pool to cap the number of workers at a reasonable level.
    greenlet_pool = Pool(size=MAX_NUM_POOL_WORKERS)

    print("Consumer daemon started, waiting for jobs...")
    print("Worker pool size: %d" % greenlet_pool.size)

    while True:
        # Since subscriber.recv() blocks when no messages are available,
        # this loop stays under control. If something is available and the
        # greenlet pool has greenlets available for use, work gets done.
        greenlet_pool.spawn(worker, subscriber.recv())

def worker(job_json):
    """
    For every incoming message, this worker function is called. Be extremely
    careful not to do anything CPU-intensive here, or you will see blocking.
    Sockets are async under gevent, so those are fair game.
    """
    # Receive raw market JSON strings.
    market_json = zlib.decompress(job_json)
    # Un-serialize the JSON data to a Python dict.
    market_data = simplejson.loads(market_json)
    # Save to your choice of DB here.
    if market_data['resultType'] == 'orders':
        rows = market_data['rowsets']
        try:
            for row in rows:
                if len(row['rows']) == 0:
                    pass
                genTime = dateutil.parser.parse(row['generatedAt'])
                genTime = int(time.mktime(genTime.timetuple()))
                typeID = row['typeID']
                regionID = row['regionID']
                buyCount = []
                sellCount = []
                buyPrice = []
                sellPrice = []
                tempMask = []
                buyAvg = 0
                buyMean = 0
                buyTotal = 0
                sellAvg = 0
                sellMean = 0
                sellTotal = 0
                set = 0
                stuff = row['rows']
                for data in stuff:
                    if data[6] == True:
                        buyPrice.append(data[0])
                        buyCount.append(data[4] - data[1])
                    elif data[6] == False:
                        sellPrice.append(data[0])
                        sellCount.append(data[4] - data[1])
                    else:
                        pass
                if len(buyPrice) > 1:
                    top = stats.scoreatpercentile(buyPrice, 95)
                    bottom = stats.scoreatpercentile(buyPrice, 5)
                    buyMasked = ma.masked_outside(buyPrice, bottom, top)
                    tempMask = buyMasked.mask
                    buyCountMasked = ma.array(buyCount, mask=tempMask, fill_value = 0)
                    ma.fix_invalid(buyMasked, mask=0)
                    ma.fix_invalid(buyCountMasked, mask=0)
                    buyAvg = ma.average(buyMasked, 0, buyCountMasked)
                    buyMean = ma.mean(buyMasked)
                    buyTotal = ma.sum(buyCountMasked)
                    if buyTotal == 0:
                        buyAvg = 0
                        buyMean = 0
                    set = 1
                    if len(buyPrice) < 4:
                        buyAvg = ma.average(buyPrice)
                        buyMean = ma.mean(buyPrice)
                        
                if len(sellPrice) > 3:
                    top = stats.scoreatpercentile(sellPrice, 95)
                    bottom = stats.scoreatpercentile(sellPrice, 5)
                    sellMasked = ma.masked_outside(sellPrice, bottom, top)
                    tempMask = sellMasked.mask
                    sellCountMasked = ma.array(sellCount, mask=tempMask, fill_value = 0)
                    ma.fix_invalid(sellMasked, mask=0)
                    ma.fix_invalid(sellCountMasked, mask=0)
                    sellAvg = ma.average(sellMasked, 0, sellCountMasked)
                    sellMean = ma.mean(sellMasked)
                    sellTotal = ma.sum(sellCountMasked)
                    if sellTotal == 0:
                        sellAvg = 0
                        sellMean = 0
                    set = 1
                    if len(sellPrice) < 4:
                        sellMean = ma.mean(sellPrice)
                        sellTotal = ma.sum(sellPrice)

                print ("ItemID: %s RegionID: %s Buy Avg: %.2f Buy Median: %.2f Buy Count: %i Sell Avg: %.2f Sell Mean: %.2f Sell Count: %i" % (typeID, regionID, np.nan_to_num(buyAvg), np.nan_to_num(buyMean), np.nan_to_num(buyTotal), np.nan_to_num(sellAvg), np.nan_to_num(sellMean), np.nan_to_num(sellTotal)))
        except:
            pass

cProfile.run('main()', 'out')

if __name__ == '__main__':
    main()
