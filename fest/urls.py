from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from fest.views import score, rateMe, home, result_action, ItemListView, ItemDetailScoreView, ItemDetailView, confirm_rating, save_score
from django.contrib import admin
from django.contrib.auth.views import logout
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^score/$', score, name='items'),
    url(r'^report/$', ItemListView.as_view(), name='item_report'),
    url(r'^report/(?P<pk>\d+)$', ItemDetailView.as_view(), name='item_rating_report'),
    url(r'^score/(?P<pk>\d+)$', ItemDetailScoreView.as_view(), name='item_jury_scoring'),
    url(r'^score/save$', save_score, name='save_score'),
    url(r'^resultaction/$', result_action, name='resultaction'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rate/$', rateMe, name='rating'),
    url(r'^rating/confirm$', confirm_rating, name='confirm_rating'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += patterns('',
        (r'^files/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)


