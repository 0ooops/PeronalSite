from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all_items/', views.all_items, name='all_items'),
    url(r'^today_items/', views.today_items, name='today_items'),
]