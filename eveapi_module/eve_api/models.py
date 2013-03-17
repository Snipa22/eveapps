from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

class apiKeys(models.model):
    id = models.IntegerField(unique=True)
    vCode = models.CharField(max_length=72)
    keyType = models.BooleanField()
    active = models.BooleanField()

class apiCharacters(models.model):
    id = models.IntegerField(unique=True)
    name = models.ForeignKey(apiNameLookup)
    key = models.ForeignKey(apiKeys)
    corpID = models.ForeignKey(apiCorp)
    allianceID = models.ForeignKey(apiAlliance, blank=True, null=True)

class apiNameLookup(models.model):
    id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

class apiCorp(models.model):
    id = models.IntegerField(unique=True)
    name = models.ForeignKey(apiNameLookup)
    ceo = models.ForeignKey(apiNameLookup)
    allianceID = models.ForeignKey(apiAlliance, blank=True, null=True)
    members = models.IntegerField()
    ticker = models.CharField(max_length=10)

class apiAlliance(models.model):
    id = models.IntegerField(unique=True)
    name = models.ForeignKey(apiNameLookup)
    members = models.IntegerField()
    executor = models.ForeignKey(apiCorp)
    ticker = models.CharField(max_length=10)