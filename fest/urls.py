from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from fest.views import score, rateMe, home, result_action, ItemListView, ItemDetailScoreView, ItemDetailView, confirm_rating, save_score, SpecialAwardListView
from django.contrib import admin
from django.contrib.auth.views import logout, password_change, password_change_done
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^score/$', score, name='items'),
    url(r'^awards/$', SpecialAwardListView.as_view(), name='awards'),
    url(r'^report/$', ItemListView.as_view(), name='item_report'),
    url(r'^report/(?P<pk>\d+)$', ItemDetailView.as_view(), name='item_rating_report'),
    url(r'^score/(?P<pk>\d+)$', ItemDetailScoreView.as_view(), name='item_jury_scoring'),
    url(r'^score/save$', save_score, name='save_score'),
    url(r'^resultaction/$', result_action, name='resultaction'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rate/$', rateMe, name='rating'),
    url(r'^rating/confirm$', confirm_rating, name='confirm_rating'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^password/$', password_change,{'template_name':'password_change_form.html'}, name='change_password'),
    #url(r'^password/$', password_change, name='change_password'),
    url(r'^password/done$', password_change_done,{'template_name':'password_change_done.html'}, name='password_change_done'),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += patterns('',
        (r'^files/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)


