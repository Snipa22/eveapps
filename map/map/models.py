from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.forms import ModelForm

WHTYPES = (
            ('A239', 'A239'),
            ('A641', 'A641'),
            ('A982', 'A982'),
            ('B041', 'B041'),
            ('B274', 'B274'),
            ('B449', 'B449'),
            ('B520', 'B520'),
            ('C125', 'C125'),
            ('C140', 'C140'),
            ('C247', 'C247'),
            ('C248', 'C248'),
            ('C391', 'C391'),
            ('D364', 'D364'),
            ('D382', 'D382'),
            ('D792', 'D792'),
            ('D845', 'D845'),
            ('E175', 'E175'),
            ('E545', 'E545'),
            ('G024', 'G024'),
            ('H121', 'H121'),
            ('H296', 'H296'),
            ('H900', 'H900'),
            ('I182', 'I182'),
            ('J244', 'J244'),
            ('K162', 'K162'),
            ('K329', 'K329'),
            ('K346', 'K346'),
            ('L477', 'L477'),
            ('L614', 'L614'),
            ('M267', 'M267'),
            ('M555', 'M555'),
            ('M609', 'M609'),
            ('N062', 'N062'),
            ('N110', 'N110'),
            ('N290', 'N290'),
            ('N432', 'N432'),
            ('N766', 'N766'),
            ('N770', 'N770'),
            ('N944', 'N944'),
            ('N968', 'N968'),
            ('O128', 'O128'),
            ('O477', 'O477'),
            ('O883', 'O883'),
            ('P060', 'P060'),
            ('Q317', 'Q317'),
            ('R051', 'R051'),
            ('R474', 'R474'),
            ('R943', 'R943'),
            ('S047', 'S047'),
            ('S199', 'S199'),
            ('S804', 'S804'),
            ('T405', 'T405'),
            ('U210', 'U210'),
            ('U319', 'U319'),
            ('U574', 'U574'),
            ('V283', 'V283'),
            ('V301', 'V301'),
            ('V753', 'V753'),
            ('V911', 'V911'),
            ('W237', 'W237'),
            ('X702', 'X702'),
            ('X877', 'X877'),
            ('Y683', 'Y683'),
            ('Y790', 'Y790'),
            ('Z060', 'Z060'),
            ('Z142', 'Z142'),
            ('Z457', 'Z457'),
            ('Z647', 'Z647'),
            ('Z971', 'Z971'),
            )

class sigs(models.model):
    SIGTYPES = (
                ('grav', 'Gravimetric'),
                ('radr', 'Radar'),
                ('ladr', 'Ladar'),
                ('magn', 'Magnetometric'),
                ('unkn', 'Wormhole'),
                )
    sigid = models.CharField(max_length=7)
    sigtype = models.CharField(max_lenth=4, choices=SIGTYPES, default='unkn')
    destination = models.CharField(max_length=10)
    type = models.CharField()
    scantime = models.DateTime(auto_now=True)
    exipretime = models.DateTime(blank=True, null=True)
    scanUser = models.IntegerField()
    location = models.CharField()

class whspace(models.model):
    WHEFFECTS = (
                 ('b', 'Black Hole'),
                 ('m', 'Magnetar'),
                 ('p', 'Pulsar'),
                 ('w', 'Wolf Rayet'),
                 ('c', 'Magnetar'),
                 ('r', 'Red Giant'),
                 ('n', 'None'),
                 )
    DANGERLEVEL = (
                   (0, 'None'),
                   (1, 'Light Concern'),
                   (2, 'Moderate Warning'),
                   (3, 'High Danger'),
                   (4, 'Collapse Immedately'),
                   )
    whid = models.CharField(max_length=10)
    owner = models.CharField(max_length=10)
    whclass = models.IntegerField()
    static = models.CharField(max_length=4, choices=WHTYPES, blank=True, null=True)
    static2 = models.CharField(max_length=4, choices=WHTYPES, blank=True, null=True)
    wheffect = models.CharField(max_length=1, choices=WHEFFECTS)
    owner = models.CharField(blank=True, null=True)
    danger = models.IntegerField(max_length=1, choices=DANGERLEVEL, default=0)
    kills = models.IntegerField(default=0)
    activity = models.IntegerField(max_length=1, choices=DANGERLEVEL, default=0)

class wormholes(models.model):
    whtype = models.ForeignKey(whdetails)
    sig = models.ForeignKey(sigs)
    massleft = models.IntegerField()
    link = models.CharField()

class whdetails(models.model):
    WHTIMERS = (
                (0, '0h'),
                (1, '16h'),
                (2, '24h'),
                (3, '48h'),
                )
    whtype = models.CharField(max_length=4, choices=WHTYPES)
    maxmass = models.IntegerField()
    maxtime = models.IntegerField(choices=WHTIMERS, default=1)
    jumpmass = models.IntegerField()