from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^snap/', views.snap, name='snap'),
	url(r'^jupyter/', views.jupyter, name='jupyter'),
	url(r'^monitor/', views.monitor, name='monitor'),
	url(r'^rest/$', views.rest, name='rest'),
	url(r'^rest/raw/$', views.rest_raw, name='rest'),
	url(r'^rest/state/$', views.rest_state, name='rest'),
	url(r'^settings/$', views.configuration, name='configuration'),
	url(r'^settings/wifi_add/$', views.wifi_add, name='wifi_add'),
	url(r'^settings/wifi_suppr/$', views.wifi_suppr, name='wifi_suppr'),
	url(r'^settings/wifi_restart/$', views.wifi_restart, name='wifi_restart'),
	url(r'^reboot/', views.reboot, name='reboot'),
	url(r'^logs/$', views.logs, name='logs'),
	url(r'^logs/raw/$', views.rawlogs, name='rawlogs'),
	url(r'^shutdown/', views.shutdown, name='shutdown'),
]