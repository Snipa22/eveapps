from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from django_authopenid.urls import urlpatterns as authopenid_urlpatterns
from registration.forms import RegistrationFormUniqueEmail

admin.autodiscover()

urlpatterns = patterns('',
    # Admin
    (r'^admin/', include(admin.site.urls)),

    (r'^map/', include(map.urls)),
)