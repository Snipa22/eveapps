from django.conf.urls.defaults import *

from eve_api import views as eveAPIViews

urlpatterns = patterns('',
    # API App Home
    url('^$', eveAPIViews.index, name='index'),
)