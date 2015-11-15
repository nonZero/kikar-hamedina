from django.conf.urls import patterns, include, url
from django.contrib import admin
# from core.views import index
# from core.views import person
# from core.views import party
# from core.views import status

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'^api/', include('core.urls')),
                       url(r'^', include('core.urls')),
                       # url(r'^$', index, name='index'),
                       # url(r'^person/(?P<person_id>\d+)/$', person, name='person'),
                       # url(r'^party/(?P<party_id>\d+)/$', party, name='party'),
                       # url(r'^status/(?P<status_id>\d+)/$', status, name='status')
                       )
