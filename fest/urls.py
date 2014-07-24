from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from fest.views import items, rateMe, home
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^items/$', items, name='items'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rate/$', rateMe, name='rating'),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += patterns('',
        (r'^files/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)


