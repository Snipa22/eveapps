"""
.. module:: eve_api.general
    :platform: Django
    :synopsis: General API calls and updates needed for pulling CCP API into a useful database form.

.. moduleAuthor:: Alexander Blair <alex@snipanet.com>
"""
# Import Models
from eve_api.models import apiCorp, apiNameLookup, apiKeyDetails, apiCharSheet, apiSkills, apiCharacters
import eveapi
import logging
import datetime

logger = logging.getLogger(__name__)

def corpAPIUpdate(corpID):
    """ Update corporation information from corp sheet as provided by CCP.

        :param corpID: CorporationID to be processed
        :type corpID: Int.
        :return: None
        :raises: None
    """
    corpData = apiHandler('corp', 'CorporationSheet', ids=corpID)
    try:
        corp = apiCorp.objects.get(id=corpID)
        corp.members = corpData.memberCount
        if corp.ceo != corpData.ceoID:
            nameUpdate(corpData.ceoID)
            corp.ceo = apiNameLookup.objects.get(id=corpData.ceoID)
    except:
        nameUpdate(corpData.ceoID)
        nameUpdate(corpData.corporationID)
        corp = apiCorp(id=corpData.corpID, name=apiNameLookup.objects.get(id=corpData.corporationID), ceo=apiNameLookup.objects.get(id=corpData.ceoID), members=corpData.memberCount, ticker=corpData.ticker, allianceID=corpData.allianceID)
    corp.save()

def nameUpdate(dataID):
    """ Inserts/updates the ID/Name mapping inside of the database from CCP.  Checks for local caches first

        :param dataID: Corp/Name/Alliance ID to be processed
        :type dataID: Int.
        :return: None
        :raises: None
    """
    if apiNameLookup.objects.filter(id=dataID).count() == 1:
        return
    result = apiHandler('eve', 'CharacterName', idlist=dataID)
    for row in result.characters:
        name = apiNameLookup(id=dataID, name=row.name)
        name.save()

def getKeyInfo(id, key):
    """ Download and store key information.  Stores the following:
        keyMask - Access Mask
        keyExpire - Key Expiration Date/time
        keyType - Type of API key - 0=Account, 1=Character, 2=Corporation
        Also calls a character sheet update on the character.  View updateCharSheet for details

        :param id: apiKey to be updated
        :type id: Int.
        :param key: vCode for the provided API key
        :type key: Str.
        :return: keyType and keyMask in a dict
        :raises: None
    """
    keyInfo = apiHandler('account', 'APIKeyInfo', keyID=id, vCode=key)
    keyType = 0
    keyMask = keyInfo.key.accessMask
    keyExpire = strptime(keyInfo.key.expires, "%Y-%m-%d %H:%M:%S")
    if keyInfo.key.type == "Character":
        keyType = 1
    elif keyInfo.key.type == "Corporation":
        keyLevel = 2
    try:
        livekey = apiKeyDetails.objects.get(keyid=id)
        livekey.keyType=keyType
        livekey.keyMask=keyMask
        livekey.keyExpire=keyExpire
        if keyLevel == 2:
            livekey.keyOwner=keyInfo.key.characters[0].corporationID
    except:
        if keyLevel == 2:
            livekey = apiKeyDetails(keyid=apiKeys.objects.get(id=keyID), keyType=keyType, keyMask=keyMask, keyExpire=keyExpire, keyOwner=keyInfo.key.characters[0].corporationID)
        else:
            livekey = apiKeyDetails(keyid=apiKeys.objects.get(id=keyID), keyType=keyType, keyMask=keyMask, keyExpire=keyExpire)
    livekey.save()
    if keyLevel != 2:
        for char in keyInfo.key.characters:
            try:
                characcess = apiCharacters.objects.get(id = char.characterID)
                corpAPIUpdate(char.corporationID)
                characcess.corpID = apiCorp.objects.get(id=char.corporationID)
            except:
                nameUpdate(char.characterID)
                corpAPIUpdate(char.corporationID)
                characcess = apiCharacters(id = char.characterID, name=apiNameLookup.objects.get(id=char.characterID), key=livekey, corpID=apiCorp.objects.get(id=char.corporationID))
            characcess.save()
            updateCharSheet(keyID, vCode, char.characterID, characcess)
    return({"keyType": keyType, "keyMask": keyMask})

def updateCharSheet(keyID, vCode, chrID, chrDB):
    """ CharacterSheet/skills Update from API.

        :param keyID: apiKey for authentication
        :type keyID: Int.
        :param vCode: vCode for the provided API key
        :type vCode: Str.
        :param chrID: CharacterID for processing
        :type chrID: Int.
    """
    chrSheet = apiHandler('char', 'CharacterSheet', keyID, vCode, chrID)
    corpAPIUpdate(chrSheet.corporationID)
    totalSP = 0
    for skill in chrSheet.skills:
        totalSP += skill.skillpoints
        try:
            skilldb = apiSkills.objects.get(skillID=skill.TypeID, charID=chrID)
            skilldb.skillLevel = skill.level
        except:
            skilldb = apiSkills(charID=chrDB, skillID=skill.TypeID, skillLevel=skill.level)
        skilldb.save()
    try:
        charapi = apiCharSheet.objects.get(charID = chrID)
        charapi.skillPoints = totalSP
        charapi.cloneSkillPoints = chrSheet.cloneSkillPoints
    except:
        charapi = apiCharSheet(charID=apiCharacters.objects.get(id=chrID), skillPoints=totalSP, cloneSkillPoints=chrSheet.cloneSkillPoints)
    charapi.save()

def apiHandler(apiType, call, keyID=0, vCode=0, ids=0):
    """ Wrapper for the API to deal with API errors

        :param apiType: The API level (eve/character/etc.)
        :type apiType: int.
        :param call: The specific API call
        :type call: Str.
        :param keyID: apiKey for authentication
        :type keyID: Int.
        :param vCode: vCode for the provided API key
        :type vCode: Str.
        :param ids: Ids that needs to be passed
        :type ids: Int.
        :return: keyType and keyMask in a dict
        :raises: None
    """
    api = eveapi.EVEAPIConnection()
    apiaccess = getattr(api, apiType + "/" + call)
    try:
        if call == 'CharacterName':
            result = apiaccess(ids=ids)
        elif call == 'CorporationSheet':
            result = apiaccess(corporationID=ids)
        elif apiType == 'char':
            result = apiaccess(keyID=keyID, vCode=vCode, userID=ids)
        elif call == 'AllianceList':
            result = apiaccess()
        else:
            result = apiaccess(keyID=keyID, vCode=vCode)
        return result
    except eveapi.Error, e:
        print "Oops! eveapi returned the following error:"
        print "code:", e.code
        print "message:", e.message