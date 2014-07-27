from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from fest.views import score, rateMe, home, report, result_action, ItemListView
from django.contrib import admin, auth
from django.contrib.auth.views import logout
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^score/$', score, name='items'),
    url(r'^report/$', report, name='report'),
    url(r'^report/items/$', ItemListView.as_view(), name='item_report'),
    url(r'^resultaction/$', result_action, name='resultaction'),
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^rate/$', rateMe, name='rating'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += patterns('',
        (r'^files/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)


