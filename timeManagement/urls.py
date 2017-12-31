from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all_items/', views.all_items, name='all_items'),
    url(r'^all_items_new/$', views.all_items_new, name='all_items_new'),
    url(r'^all_items_edit/(?P<pk>\d+)/$', views.all_items_edit, name='all_items_edit'),
    url(r'^today_items/', views.today_items, name='today_items'),
    url(r'^today_items_new/$', views.today_items_new, name='today_items_new'),
    url(r'^today_items_edit/(?P<pk>\d+)/$', views.today_items_edit, name='today_items_edit'),
]