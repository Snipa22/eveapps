#!/usr/bin/env python
from bottle import route, run, request, abort
import PySQLPool
from xml.dom.minidom import Document
from config import config
import locale
import pylibmc
import threading
import sys
import time

PySQLPool.getNewPool().maxActiveConnections = 100
PySQLPool.getNewPool().maxActivePerConnection = 1
mc = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})
pool = pylibmc.ClientPool()
db = PySQLPool.getNewConnection(user=config['username'],passwd=config['password'],db=config['db'])
locale.setlocale(locale.LC_ALL, 'en_US')
maxThreads = 60
pool.fill(mc, maxThreads + 10)
repoList = []
repoVal = {}

def repoThread():
    global repoList
    global repoVal
    while len(repoList) > 0:
        row = repoList.pop()
        regions = regionList()
        prices = getMineralBasket()
        refValue = ((row['Tritanium'] * prices['Tritanium']['sellavg']) +
        (row['Pyerite'] * prices['Pyerite']['sellavg']) +
        (row['Mexallon'] * prices['Mexallon']['sellavg']) +
        (row['Isogen'] * prices['Isogen']['sellavg']) +
        (row['Nocxium'] * prices['Nocxium']['sellavg']) +
        (row['Zydrine'] * prices['Zydrine']['sellavg']) +
        (row['Megacyte'] * prices['Megacyte']['sellavg']) +
        (row['Morphite'] * prices['Morphite']['sellavg'])) / row['portion']
        queryValue = PySQLPool.getNewQuery(db)
        stuff = refValue * 1.02
        queryValue.Query("""SELECT region, sellavg, sell, buy, buyavg from prices where itemid = %s""" % (row['typeID'],))
        for rowValue in queryValue.record:
            if rowValue['sellavg'] > stuff:
                continue
            if rowValue['sellavg'] != 0 and refValue/rowValue['sellavg'] * 100 > 100:
                repoVal[regions[rowValue['region']]][itemName(row['typeID'])] = {'sellavg': rowValue['sellavg'], 'sell': rowValue['sell'], 'buy': rowValue['buy'], 'buyavg': rowValue['buyavg'], 'refprice': refValue, 'percentage': refValue/rowValue['sellavg']* 100}
            elif rowValue['sellavg'] == 0 and rowValue['sell'] != 0 and refValue/rowValue['sell'] * 100 > 100:
                repoVal[regions[rowValue['region']]][itemName(row['typeID'])] = {'sellavg': rowValue['sellavg'], 'sell': rowValue['sell'], 'buy': rowValue['buy'], 'buyavg': rowValue['buyavg'], 'refprice': refValue, 'percentage': refValue/rowValue['sell'] * 100}
            else:
                continue

def getMineralBasket(region = 10000002):
    try:
        with pool.reserve() as mc:
            basket = mc.get("basket" + str(region))
        if basket != None:
            return basket
    except:
        pass
    query = PySQLPool.getNewQuery(db)
    query.Query("""SELECT * from prices where (itemid BETWEEN 34 and 40 or itemid = 11399) and region = '%i'""" % (region))
    retVal = {}
    for row in query.record:
        intQuery = PySQLPool.getNewQuery(db)
        intQuery.Query("""SELECT typeName from eve.invTypes where typeID = %i""" % (row['itemid']))
        for name in intQuery.record:
            typeName = name['typeName']
        retVal[typeName] = row
    with pool.reserve() as mc:
        mc.set("basket" + str(region), retVal, time=600)
    return retVal


def regionName(id):
    query = PySQLPool.getNewQuery(db)
    query.Query("""SELECT regionName from eve.mapRegions where regionID = %s""", (id,))
    if len(query.record) != 1:
        return None
    for row in query.record:
        return row['regionName']

def regionID(id):
    query = PySQLPool.getNewQuery(db)
    query.Query("""SELECT regionID from eve.mapRegions where regionName = %s""", (id,))
    if len(query.record) != 1:
        return None
    for row in query.record:
        return row['regionID']

def regionList():
    try:
        with pool.reserve() as mc:
            regions = mc.get("regions")
        if regions != None:
            return regions
    except:
        pass
    query = PySQLPool.getNewQuery(db)
    query.Query("""SELECT regionID, regionName from eve.mapRegions""")
    retVal = {}
    for row in query.record:
        retVal[int(row['regionID'])] = row['regionName']
    with pool.reserve() as mc:
        mc.set("regions", retVal)
    return retVal

def itemName(id):
    try:
        with pool.reserve() as mc:
            name = mc.get("itemName" + str(id))
        if name != None:
            return name
    except:
        pass
    query = PySQLPool.getNewQuery(db)
    query.Query("""SELECT typeName from eve.invTypes where typeID = %s""", (id,))
    if len(query.record) != 1:
        return None
    for row in query.record:
        with pool.reserve() as mc:
            mc.set("itemName" + str(id), row['typeName'])
        return row['typeName']

def regionStatus(id):
    query = PySQLPool.getNewQuery(db)
    query.Query("""SELECT factionID from eve.mapRegions where regionID = %s and factionID is not null""", (id,))
    if len(query.record) == 1:
        return True
    return None

@route('/region/<id:int>')
def regionData(id):
    if regionName(id):
        doc = Document()
        prices = doc.createElement("prices")
        doc.appendChild(prices)
        query = PySQLPool.getNewQuery(db)
        query.Query("""select SQL_NO_CACHE eve.invTypes.typeName as itemName, app.prices.* from app.prices left join eve.invTypes on app.prices.itemid = eve.invTypes.typeID where app.prices.region = %s order by eve.invTypes.typeName asc""", (id,))
        for row in query.record:
            item = doc.createElement("item")
            item.setAttribute("name", row['itemName'])
            item.setAttribute("buyMean", str(row['buymean']))
            item.setAttribute("buyAvg", str(row['buyavg']))
            item.setAttribute("sellMean", str(row['sellmean']))
            item.setAttribute("sellAvg", str(row['sellavg']))
            item.setAttribute("buy", str(row['buy']))
            item.setAttribute("sell", str(row['sell']))
            prices.appendChild(item)
        return doc.toprettyxml(indent="")

@route('/reposearch')
def repoSearch():
    global repoList
    global repoVal
    query = PySQLPool.getNewQuery(db)
    prices = getMineralBasket(10000030)
    regions = regionList()
    for data in regions:
        repoVal[regions[data]] = {}
    query.Query("SELECT * FROM repromin where rate > 5")
    for row in query.record:
        repoList.append(row)
        
    threads = []
    for i in range(maxThreads):
        """Worker scanning system"""
        t = threading.Thread(target=repoThread, args=())
        threads.append(t)
        time.sleep(.1)
        t.start()

    while threading.activeCount()>1:
        """Verification of the number of active theads for monitoring purposes."""
        time.sleep(1)
        print "Active threads: %i/%i" % (threading.activeCount() - 1, maxThreads)
        sys.stdout.flush()

    output = """<html><head><script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://snipanet.com/inc/jquery.tablesorter.min.js"></script>
    <link rel="stylesheet" href="http://snipanet.com/inc/themes/blue/style.css" type="text/css">
    <script type="text/javascript">
    $(document).ready(function() 
    { 
    """
    for num in range(len(repoVal)):
        output += """$("#myTable%i").tablesorter();""" % (num,)
    output += """}
    ); 
    </script>
    </head><body>
    """
    incNum = 0;
    for region in repoVal:
        data = repoVal[region]
        if len(data) == 0 or regionStatus(regionID(region)) == None or data[prices]['percentage'] < 100:
            continue
        output += """Region: %s<br><table id="myTable%i" class="tablesorter"><thead><tr><th>Item Name</th><th>Sell Avg</th><th>Sell Price</th><th>Buy Avg</th><th>Buy Price</th><th>Refine Price</th><th>Refine Percentage</tr></thead><tbody>""" % (region, incNum)
        for prices in data:
            output += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%.2f%%</td></tr>" % (prices, locale.format("%.2f", data[prices]['sellavg'], grouping=True), locale.format("%.2f", data[prices]['sell'], grouping=True), locale.format("%.2f", data[prices]['buyavg'], grouping=True), locale.format("%.2f", data[prices]['buy'], grouping=True), locale.format("%.2f", data[prices]['refprice'], grouping=True), data[prices]['percentage'])
        output += "</tbody></table><br><br>"
        incNum += 1
    return output

@route('/repoapi')
def repoApi():
    retVal = {}
    doc = Document()
    refitems = doc.createElement("refitems")
    doc.appendChild(refitems)
    query = PySQLPool.getNewQuery(db)
    prices = getMineralBasket(10000030)
    query.Query("SELECT * FROM repromin where rate > 3")
    for row in query.record:
        item = doc.createElement("item")
        refValue = ((row['Tritanium'] * prices['Tritanium']['sellavg']) +
        (row['Pyerite'] * prices['Pyerite']['sellavg']) +
        (row['Mexallon'] * prices['Mexallon']['sellavg']) +
        (row['Isogen'] * prices['Isogen']['sellavg']) +
        (row['Nocxium'] * prices['Nocxium']['sellavg']) +
        (row['Zydrine'] * prices['Zydrine']['sellavg']) +
        (row['Megacyte'] * prices['Megacyte']['sellavg']) +
        (row['Morphite'] * prices['Morphite']['sellavg'])) / row['portion'] * .95
        item.setAttribute("typeID", str(row['typeID']))
        refitems.appendChild(item)
        item.appendChild(doc.createTextNode(str(refValue)))
    return doc.toprettyxml(indent="")

run(host='127.0.0.1', port=8080)
