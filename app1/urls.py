from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^snap/', views.snap, name='snap'),
	url(r'^jupyter/', views.jupyter, name='jupyter'),
	url(r'^settings/$', views.settings, name='configuration'),
	url(r'^settings/change/$', views.change, name='wifi'),
	url(r'^juju/', views.juju, name='juju'),
	url(r'^juju2/', views.juju2, name='juju2'),
]