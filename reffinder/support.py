#!/usr/bin/env python
import PySQLPool
from config import config
# Supporting functions/one time user functions for the Eve-Refine-Finder

db = PySQLPool.getNewConnection(user=config['username'],passwd=config['password'],db=config['db'], commitOnEnd=True)

queryText = """SELECT
t1.typeID,
(t1.volume * t1.portionSize) as Volume,
t1.portionSize,
SUM(CASE WHEN m1.materialTypeID = 34 THEN m1.quantity ELSE 0 END) AS Tritanium,
SUM(CASE WHEN m1.materialTypeID = 35 THEN m1.quantity ELSE 0 END) AS Pyerite,
SUM(CASE WHEN m1.materialTypeID = 36 THEN m1.quantity ELSE 0 END) AS Mexallon,
SUM(CASE WHEN m1.materialTypeID = 37 THEN m1.quantity ELSE 0 END) AS Isogen,
SUM(CASE WHEN m1.materialTypeID = 38 THEN m1.quantity ELSE 0 END) AS Nocxium,
SUM(CASE WHEN m1.materialTypeID = 39 THEN m1.quantity ELSE 0 END) AS Zydrine,
SUM(CASE WHEN m1.materialTypeID = 40 THEN m1.quantity ELSE 0 END) AS Megacyte,
SUM(CASE WHEN m1.materialTypeID = 11399 THEN m1.quantity ELSE 0 END) AS Morphite
FROM eve.invTypes t1
INNER JOIN eve.dgmTypeAttributes t2 ON t1.typeID = t2.typeID AND t2.attributeID = 633 AND t1.published = 1 AND t2.valueInt IN (0, 1, 2, 3, 4) -- metaLevel
INNER JOIN eve.invGroups t3 ON t1.groupID = t3.groupID
INNER JOIN eve.invTypeMaterials m1 ON t1.typeID = m1.typeID
GROUP BY
t1.typeID,
t1.typeName,
coalesce(t2.valueFloat,t2.valueInt),
t1.groupID,
t3.groupName,
t1.volume,
t1.portionSize,
t1.basePrice
ORDER BY t1.typeID"""
query = PySQLPool.getNewQuery(db)
query.Query(queryText)
for row in query.record:
    if (row['Tritanium'] + row['Pyerite'] + row['Mexallon'] + row['Isogen'] + row['Nocxium'] + row['Zydrine'] + row['Megacyte'] + row['Morphite'])/100 < row['Volume']:
        pass
    newQuery = "insert into `repromin` (`typeID`,`Volume`,`Tritanium`,`Pyerite`,`Mexallon`,`Isogen`,`Nocxium`,`Zydrine`,`Megacyte`,`Morphite`, `rate`, `portion`) VALUES (%i,%f,%i,%i,%i,%i,%i,%i,%i,%i,%f,%i)" % (row['typeID'], row['Volume'], row['Tritanium'], row['Pyerite'], row['Mexallon'], row['Isogen'], row['Nocxium'], row['Zydrine'], row['Megacyte'], row['Morphite'], ((float(row['Tritanium'] + row['Pyerite'] + row['Mexallon'] + row['Isogen'] + row['Nocxium'] + row['Zydrine'] + row['Megacyte'] + row['Morphite'])/100)/row['Volume']), row['portionSize'])
    query.Query(newQuery)
