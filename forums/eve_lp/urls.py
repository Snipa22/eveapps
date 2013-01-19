from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # LP App Home
    url('^$', lp_views.index, name='index'),
    # LP App Corp
    url('^corp/(\d{7})$', lp_views.corp, name='corp'),
)
