from django.conf.urls.defaults import *

from eve_api import views as eveAPIViews

urlpatterns = patterns('',
    # LP App Home
    url('^$', eveAPIViews.index, name='index'),
    # LP App Corp
    url('^corp/(\d{7})$', eveAPIViews.corp, name='corp'),
)