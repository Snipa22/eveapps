# Import Models
from eve_api.models import apiAlliance, apiCorp, apiNameLookup
from eve_api.general import corpAPIUpdate, nameUpdate
import eveapi

class Command(BaseCommand):
    api = eveapi.EVEAPIConnection()
    result = api.eve.AllianceList()
    for allianceData in result.alliances:
        try:
            alliance = apiAlliance.objects.get(id=allianceData.allianceID)
            alliance.members = allianceData.memberCount
            if alliance.executor != allianceData.executorCorpID
                corpAPIUpdate(allianceData.executorCorpID)
                alliance.executor = apiCorp.objects.get(id=allianceData.executorCorpID)
            alliance.save()
        except:
            corpAPIUpdate(allianceData.executorCorpID)
            nameUpdate(allianceData.AllianceID)
            alliance = apiAlliance(id=allianceData.AllianceID, name=apiNameLookup.objects.get(id=allianceData.allianceID), members=allianceData.memberCount, executor=apiCorp.objects.get(id=allianceData.executorCorpID), ticker=allianceData.shortName)
            alliance.save()