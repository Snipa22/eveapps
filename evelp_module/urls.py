from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


urlpatterns = patterns('',
    (r'^lp/', include('eve_lp.urls')),
)
