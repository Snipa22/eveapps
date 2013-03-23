from django.conf.urls.defaults import *

from map import views as mapViews

urlpatterns = patterns('',
    # API App Home
    url('^$', mapViews.index, name='index'),
)