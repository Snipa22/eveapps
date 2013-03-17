# Import Models
from eve_api.models import apiCorp, apiNameLookup
import eveapi
import logging

logger = logging.getLogger(__name__)

api = eveapi.EVEAPIConnection()

def corpAPIUpdate(corpID):
    try:
        corpData = api.corp.CorporationSheet(corporationID=corpID)
    except eveapi.Error, e:
        print "Oops! eveapi returned the following error:"
        print "code:", e.code
        print "message:", e.message
    try:
        corp = apiCorp.objects.get(id=corpID)
        corp.members = corpData.memberCount
        if corp.ceo != corpData.ceoID
            nameUpdate(corpData.ceoID)
            corp.ceo = apiNameLookup.objects.get(id=corpData.ceoID)
        corp.save()
    except:
        nameUpdate(corpData.ceoID)
        nameUpdate(corpData.corporationID)
        corp = apiCorp(id=corpData.corpID, name=apiNameLookup.objects.get(id=corpData.corporationID), ceo=apiNameLookup.objects.get(id=corpData.ceoID), members=corpData.memberCount, ticker=corpData.ticker, allianceID=corpData.allianceID)
        corp.save()

def nameUpdate(dataID):
    if apiNameLookup.objects.filter(id=dataID).count() == 1:
        return
    try:
        result = api.eve.CharacterName(ids=dataID)
    except eveapi.Error, e:
        print "Oops! eveapi returned the following error:"
        print "code:", e.code
        print "message:", e.message
    for row in result.characters:
        name = apiNameLookup(id=dataID, name=row.name)
        name.save()

def getKeyInfo(id, key):
    try:
        keyInfo = api.account.APIKeyInfo(keyID=id, vCode=key)
    except eveapi.Error, e:
        print "Oops! eveapi returned the following error:"
        print "code:", e.code
        print "message:", e.message
