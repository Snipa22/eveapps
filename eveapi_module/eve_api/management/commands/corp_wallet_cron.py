# Import Models
from eve_api.models import apiWallet, apiKeyDetails
import eveapi
from django.db.models import Q

class Command(BaseCommand):
    keys = apiKeyDetails.objects.get(keyType = 2)
    for key in keys:
        if key.keyid.active == False:
            continue
        try:
            apiId = key.keyid.id
            apivCode = key.keyid.vCode
            api = eveapi.EVEAPIConnection()
            for division in range(1000, 1006):
                try:
                    dbdata = apiWallet.objects.get(Q(ownerID1 = key.keyOwner) | Q(ownerID2 = key.keyOwner), division=division).order_by('date')[:1]
                    start = dbdata.refID
                except:
                    start = 0
                try:
                    apidata = api.corp.WalletJournal(keyID=apiId, vCode=apivCode, accountKey=div, fromID=start, rowcount=1000)
                except:
                    continue
                for txn in apidata.transactions:
                    if txn.refID <= start:
                        continue
                    apiWallet(refID=txn.refID, refTypeID=txn.refTypeID, ownerID1=txn.ownerID1, ownerID2=txn.ownerID2, amount=txn.amount, division=div, date=strptime(txn.date, "%Y-%m-%d %H:%M:%S"))
                    apiWallet.save()