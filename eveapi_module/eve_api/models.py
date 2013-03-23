"""
.. module:: models
    :platform: Django
    :synopsis: All models needed for the eveapi Django Module

.. moduleauthor:: Alexander Blair <alex@snipanet.com>
"""

from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.forms import ModelForm

class apiKeys(models.model):
    """Class deals with storage of API Keys, vCode

    Fields:
        id (int): ID for the API key.
        vCode (string): vCode for the API key
        active (bool): Status of API key, if enabled or disabled.  True = enabled, False = disabled
    """
    id = models.IntegerField(unique=True)
    vCode = models.CharField(max_length=120)
    active = models.BooleanField(default=True)

class apiKeysForm(ModelForm):
    class Meta:
        model = apiKeys
        exclude = ('active',)

class apiKeyDetails(models.model):
    """Class deals with all API Key Details

    Fields:
        id (ForeignKey): Links back to the main apiKeys fieldset
        keyType(int): Determines what type of APIKey this is, 0=Account, 1=Character, 2=Corporation
        keyMask(int): Stores the accessMask to the key, this is a binary value, I know.
        expire(DateTime): This is the expiration date of the key for cron usage.
        keyOwner(int): Only used in corp keys, determines the owning corp.
    """
    keyid = models.ForeignKey(apiKeys)
    keyType = models.IntegerField()
    keyMask = models.IntegerField()
    expire = models.DateTimeField()
    keyOwner = models.IntegerField(blank=True, null=True)

class apiCharacters(models.model):
    """Class deals with storage of character generics

    Fields:
        id (int): Character ID as provided by CCP.
        name (ForeignKey): Character name as stored in the apiNameLookup table
        key (ForeignKey): Determines which API key this character belongs to.
        corpID (ForeignKey): Determines what corp this character belongs to.
        allianceID (ForeignKey): Determines what alliance this character belongs to.
    """
    id = models.IntegerField(unique=True)
    name = models.ForeignKey(apiNameLookup)
    key = models.ForeignKey(apiKeys)
    corpID = models.ForeignKey(apiCorp)
    allianceID = models.ForeignKey(apiAlliance, blank=True, null=True)

class apiNameLookup(models.model):
    """Class deals with storage of Object id -> Name mapping

    Fields:
        id (int): Character ID as provided by CCP.
        name (string): Item Name as provided by CCP API
    """
    id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

class apiCorp(models.model):
    """Class deals with storage of Corp Information

    Fields:
        id (int): Corp ID as provided by CCP
        name (ForeignKey): Corp name as stored in the apiNameLookup table
        ceo (ForeignKey): Ceo name as stored in the apiNameLookup table
        allianceID (ForeignKey): Alliance ID linkage to apiAlliance
        members (int): Current number of members in the corp
        ticker (string): Corp ticker for easy searching.
    """
    id = models.IntegerField(unique=True)
    name = models.ForeignKey(apiNameLookup)
    ceo = models.ForeignKey(apiNameLookup)
    allianceID = models.ForeignKey(apiAlliance, blank=True, null=True)
    members = models.IntegerField()
    ticker = models.CharField(max_length=10)

class apiAlliance(models.model):
    """Class deals with storage of Alliance Information

    Fields:
        id (int): Alliance ID as provided by CCP
        name (ForeignKey): Alliance name as stored in the apiNameLookup table
        executor (ForeignKey): Executor Corp as stored in the apiCorp table
        members (int): Current number of members in the Alliance
        ticker (string): Corp ticker for easy searching.
    """
    id = models.IntegerField(unique=True)
    name = models.ForeignKey(apiNameLookup)
    members = models.IntegerField()
    executor = models.ForeignKey(apiCorp)
    ticker = models.CharField(max_length=10)

class apiSkills(models.model):
    """Class deals with storage of Skill information

    Fields:
        charID (ForeignKey): Link to apiCharacters
        skillID (int): SkillID as provided by CCP
        skillLevel (int): Level of the skill
    """
    charID = models.ForeignKey(apiCharacters)
    skillID = models.IntegerField()
    skillLevel = models.IntegerField()

class apiCharSheet(models.model):
    """Class deals with the storage of charsheet data, except the skills, which are in apiSkills

    Fields:
        charID (ForeignKey): Link to the apiCharacters
        skillPoints (int): Current number of SP
        cloneSkillPoints (int): SP available on clone (for warning purposes)
    """

    charID = models.ForeignKey(apiCharacters)
    skillPoints = models.IntegerField()
    cloneSkillPoints = models.IntegerField()

class apiWallet(models.model):
    """Class deals with the storage of all wallet data.

    Fields:
        refID (int): Transaction Refrence ID
        refTypeID (int): Type of Transaction
        ownerID1 (int): ID of Sender
        ownerID2 (int): ID of receiver
        amount (double): Transaction amount
        division (int): Wallet Division
        date (datetime): Date of transaction
    """
    refID = models.IntegerField(unique=True)
    refTypeID = models.IntegerField()
    ownerID1 = models.IntegerField()
    ownerID2 = models.IntegerField()
    amount = models.DoubleField()
    division = models.IntegerField()
    date = models.DateTimeField()