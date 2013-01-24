# Import Models
from eve_db.models import InvType, CrpNPCCorporation
from django.shortcuts import render_to_response
import sqlite3
from eveprices import eveprices
import cPickle as pickle

def corp(request, corpID):
    if 1000002 >= corpID >= 1000182:
        return render_to_response("eve_lp/error.html", {"error": "Invalid Corp ID"})
    prices = eveprices.eveprices()
    sqlite = sqlite3.connect('eve_lp/lpdb.db')
    c = sqlite.cursor()
    c.execute("SELECT offers.* FROM offers join corpOffers on offers.offerID = corpOffers.offerID WHERE corpOffers.corpID = ?", (corpID,))
    retVal = {}
    for row in c:
        oID = row[0]
        retVal[oID] = {'iskCost': row[2], 'typeID': row[1], 'lpCost': row[3], 'reqItems': [], 'quantity': row[5], 'itemSell': prices.getPrice(row[1], orderType='sell'), 'name': InvType.objects.get(id=row[1]).name}
        iskCost = 0
        if row[4]:
            needed_items = pickle.loads(str(row[4]))
            for item in needed_items:
                price = prices.getPrice(item[0]) * item[1]
                retVal[oID]['iskCost'] += price
                retVal[oID]['reqItems'].append({'typeID': item[0], 'quantity': item[1], 'price': price, 'name': InvType.objects.get(id=item[0]).name})
        if retVal[oID]['itemSell'] is not None:
            retVal[oID]['iskLp'] = ((retVal[oID]['itemSell'] * retVal[oID]['quantity']) - retVal[oID]['iskCost'])/retVal[oID]['lpCost']
        else:
            retVal[oID]['itemSell'] = 0
            retVal[oID]['iskLp'] = 0
    return render_to_response("eve_lp/corp.html", {'lpdata' : retVal})

def index(request):
    return "lol"
