from django.conf.urls import patterns, url
from tripapotamus import views

urlpatterns = patterns('',
                       url(r'^$', views.main, name='mainpage'),
                       url(r'^create_user/$', views.createUser, name='createaccount'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^deactivate/$', views.deactivate, name='deactivate'),
                       url(r'^addBookmark/(?P<tripID>\d+)/$', views.addBookmark, name='addBookmark'),
                       url(r'^getAmazonProducts/$', views.getAmazonProducts, name='getAmazonProducts'),
                       url(r'^deleteBookmark/(?P<bookmarkID>bookmark\d{1}_id)/$', views.deleteBookmark, name='deleteBookmark'),
                       url(r'^deleteHistoryTrip/(?P<tripID>\d{2})/$', views.deleteHistoryTrip, name='deleteHistoryTrip'),)
