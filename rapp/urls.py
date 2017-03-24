from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^$', views.logout, name='logout'),
    url(r'^statistics/$', views.stats, name='stats'),
    url(r'^lockout_list/$', views.forms_list, name='lockout_list'),
    url(r'^ra_list/$', views.ra_list, name='ra_list'),
    url(r'^halls/(?P<pk>\d+)/$', views.halls_list, name='halls'),
    url(r'^roominspection/(?P<pk>\d+)/$', views.form_detail, name='form_detail'),
    url(r'^ra/(?P<pk>\d+)/$', views.form_detail, name='form_detail'),
    url(r'^student/(?P<pk>\d+)/$', views.student_detail, name='student_detail'),
]