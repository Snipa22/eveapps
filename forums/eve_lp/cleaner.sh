#!/bin/bash
sed -r --in-place "s/u\'/\'/g" lpdump.py
sed -r --in-place "s/u\"/\"/g" lpdump.py
sed -r --in-place "s/\'sort_Required Items\': \(\d+, \(.*?\)\), //g" lpdump.py
sed -r --in-place "s/'decoClass': <class 'listentry.LPOfferEntry'>, //g" lpdump.py
sed -r --in-place "s/<KeyVal: //g" lpdump.py
sed -r --in-place "s/>,/,/g" lpdump.py
rm -rfv *.pyc
