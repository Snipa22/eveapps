from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from django_authopenid.urls import urlpatterns as authopenid_urlpatterns
from registration.forms import RegistrationFormUniqueEmail

from djangobb_forum import settings as forum_settings
from sitemap import SitemapForum, SitemapTopic


for i, rurl in enumerate(authopenid_urlpatterns):
    if rurl.name == 'registration_register':
        authopenid_urlpatterns[i].default_args.update({'form_class': RegistrationFormUniqueEmail})
        break

admin.autodiscover()

sitemaps = {
    'forum': SitemapForum,
    'topic': SitemapTopic,
}

urlpatterns = patterns('',
    # Admin
    (r'^admin/', include(admin.site.urls)),

    # Sitemap
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    # Apps
    (r'^forum/account/', include('django_authopenid.urls')),
    (r'^forum/', include('djangobb_forum.urls', namespace='djangobb')),
    (r'^lp/', include('eve_lp.urls')),
)

# PM Extension
if (forum_settings.PM_SUPPORT):
    urlpatterns += patterns('',
        (r'^forum/pm/', include('django_messages.urls')),
   )

if (settings.DEBUG):
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
            'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
