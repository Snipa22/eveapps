import sqlite3
import sys
import lpdump
import cPickle as pickle

corp = sys.argv[1]
conn = sqlite3.connect('lpdb.db')
c = conn.cursor()
lpdata = lpdump.data
for row in lpdata:
    if row['reqItems']:
        c.execute("INSERT OR REPLACE INTO offers VALUES(?, ?, ?, ?, ?, ?)", (row['offerID'], row['typeID'], row['iskCost'], row['lpCost'], pickle.dumps(row['reqItems']), row['qty']))
    else:
        c.execute("INSERT OR REPLACE INTO offers VALUES(?, ?, ?, ?, NULL, ?)", (row['offerID'], row['typeID'], row['iskCost'], row['lpCost'], row['qty']))
    c.execute("INSERT OR REPLACE INTO corpOffers VALUES(?, ?)", (corp, row['offerID']))
conn.commit()
print "Dump imported"
