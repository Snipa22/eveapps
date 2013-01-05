from flask import Flask
from flask import g, request, redirect, url_for
from functools import wraps
from DBUtils.PooledDB import PooledDB
import locale
import sys
import mysql.connector
import sqlite3
import cPickle as pickle
import pylibmc
import simplejson as json
pool_size = 20
sdePool = PooledDB(mysql.connector, pool_size, database='eve', user='eve', host='192.168.134.114', password='JQ8YtqaFPtMq91UJeF1KgqYD')
pricePool = PooledDB(mysql.connector, pool_size, database='app', user='app', host='192.168.134.114', password='JQ8YtqaFPtMq91UJeF1KgqYD')
app = Flask(__name__)
locale.setlocale(locale.LC_ALL, 'en_US')

@app.route("/")
def main():
    return "HAI 2 U"

@app.route("/lpstore/<int:corpID>")
def lpstore(corpID):
    if 1000002 >= corpID >= 1000182:
        return "Invalid Corp ID"
    retVal = {}
    c = g.sqlite.cursor()
    c.execute("SELECT offers.* FROM offers join corpOffers on offers.offerID = corpOffers.offerID WHERE corpOffers.corpID = ?", (corpID,))
    for row in c:
        oID = row[0]
        retVal[oID] = {'iskCost': row[2], 'typeID': row[1], 'lpCost': row[3], 'reqItems': [], 'quantity': row[5], 'itemSell': get_price(row[1]), 'name': getName(row[1])}
        iskCost = 0
        if row[4]:
            needed_items = pickle.loads(str(row[4]))
            for item in needed_items:
                price = get_price(item[0], 'sell') * item[1]
                retVal[oID]['iskCost'] += price
                retVal[oID]['reqItems'].append({'typeID': item[0], 'quantity': item[1], 'price': price, 'name': getName(item[0])})
        if retVal[oID]['itemSell'] is not None:
            retVal[oID]['iskLp'] = ((retVal[oID]['itemSell'] * retVal[oID]['quantity']) - retVal[oID]['iskCost'])/retVal[oID]['lpCost']
        else:
            retVal[oID]['itemSell'] = 0
            retVal[oID]['iskLp'] = 0
    output = """<html><head><script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://snipanet.com/inc/jquery.tablesorter.min.js"></script>
    <script type="text/javascript" src="https://raw.github.com/jquery/jquery-metadata/master/jquery.metadata.js"></script>
    <link rel="stylesheet" href="http://snipanet.com/inc/themes/blue/style.css" type="text/css">
    <script type="text/javascript">
    $(document).ready(function() 
    {
        $.tablesorter.addParser({
            id: 'fancyNumber',
            is:function(s){return false;},
            format: function(s) {return s.replace(/[\,\.]/g,'');},
            type: 'numeric'
        });
        $("#myTable").tablesorter();
    }
    ); 
    </script>
    <style TYPE="text/css">
    span.dropt {border-bottom: thin dotted; background: #ffeedd;}
    span.dropt:hover {text-decoration: none; background: #ffffff; z-index: 6; }
    span.dropt span {position: absolute; left: -9999px;
      margin: 20px 0 0 0px; padding: 3px 3px 3px 3px;
      border-style:solid; border-color:black; border-width:1px; z-index: 6;}
    span.dropt:hover span {left: 2%; background: #ffffff;} 
    span.dropt span {position: absolute; left: -9999px;
      margin: 4px 0 0 0px; padding: 3px 3px 3px 3px; 
      border-style:solid; border-color:black; border-width:1px;}
    span.dropt:hover span {margin: 20px 0 0 170px; background: #ffffff; z-index:6;} 
    </style>
    </head><body>
    <br><table id="myTable" class="tablesorter"><thead><tr><th>Item Name</th><th class=\"{sorter: 'fancyNumber'}\">Store Price</th><th class=\"{sorter: 'fancyNumber'}\">Market Price</th><th class=\"{sorter: 'fancyNumber'}\">LP</th><th class=\"{sorter: 'fancyNumber'}\">Isk/LP</th><th>Items Needed</th></thead><tbody>
    """
    for data in retVal:
        item = retVal[data]
        if len(item['reqItems']) == 0:
            reqitems = '0'
        else:
            stuff = "<span class='dropt'>%i<span>" % len(item['reqItems'])
            for smack in item['reqItems']:
                stuff += "Quantity: %i :: Item: %s :: %s ISK ea.<br>" % (smack['quantity'], smack['name'], locale.format("%i", smack['price'], grouping=True))
            stuff += "</span></span>"
            reqitems = stuff
        output += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (item['name'],
            locale.format("%i", item['iskCost'], grouping=True),
            locale.format("%i", item['itemSell'], grouping=True),
            locale.format("%i", item['lpCost'], grouping=True),
            locale.format("%i",item['iskLp'], grouping=True),
            reqitems)

    output += """</table></body>"""
    return output

@app.route("/suggestion")
def suggestion():
    c = g.sqlite.cursor()
    c.execute("select typeID from offers order by random() limit 10")
    output = """<script type="text/javascript"> 
        var items = new Array("""
    
    for row in c:
        output += "%i," % c[0]
    output += """34);
        var index = 0;
         
        function showMarketDetails() {
          if (isCompleted()) { 
            window.location.reload();
          } else {
            CCPEVE.showMarketDetails(items[index++]);
          }
        }
         
        function isCompleted() {
          return index >= items.length;
        }
         
        function start() {
          setInterval ( "showMarketDetails()", 2000 );
        }
         
        start();
        </script> 
"""
    return output

def get_price(typeID, type='buy'):
    retVal = 0
    try:
        curs = g.prices.cursor()
        curs.execute("SELECT * from prices where region = 10000002 AND itemid = %i" % typeID)
        data = curs.fetchone()
        bmean = data[2]
        smean = data[4]
        bavg = data[3]
        savg = data[5]
        if type == 'sell':
            if savg != 0:
                g.mc.set('price' + str(typeID) + type, savg, time=1800)
                retVal = savg
            if smean != 0:
                g.mc.set('price' + str(typeID) + type, smean, time=1800)
                retVal = smean
            if bavg != 0:
                g.mc.set('price' + str(typeID) + type, bavg, time=1800)
                retVal = bavg
            if bmean != 0:
                g.mc.set('price' + str(typeID) + type, bmean, time=1800)
                retVal = bmean
        else:
            if bavg != 0:
                g.mc.set('price' + str(typeID) + type, bavg, time=1800)
                retVal = bavg
            if bmean != 0:
                g.mc.set('price' + str(typeID) + type, bmean, time=1800)
                retVal = bmean
            if savg != 0:
                g.mc.set('price' + str(typeID) + type, savg, time=1800)
                retVal = savg
            if smean != 0:
                g.mc.set('price' + str(typeID) + type, smean, time=1800)
                retVal = smean
    except:
        retVal = 0
    if retVal is None:
        return 0
    else:
        return retVal

def getName(typeID):
    try:
        name =  g.mc.get('name' + str(typeID))
        if not name:
            raise Exception
        return name
    except:
        try:
            curs = g.sde.cursor()
            curs.execute("SELECT typeName from invTypes where typeID = %i" % typeID)
            data = curs.fetchone()
            if data[0] is not None:
                name = g.mc.set('name' + str(typeID), data[0])
                return data[0]
        except:
            return "Unknown"

@app.before_request
def before_request():
    g.mc = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})
    g.sqlite = sqlite3.connect('/home/snipa/eveapps/lpapp/lpdb.db')
    g.sde = sdePool.connection()
    g.prices = pricePool.connection()

@app.teardown_request
def teardown_request(exception):
    g.sde.close()
    g.sqlite.close()
    g.prices = pricePool.connection()

if __name__ == "__main__":
    app.run(debug=True)
