from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all/$', views.all_posts, name='all_posts'),
    url(r'^new/$', views.new_post, name='new_post'),
    url(r'^details/(?P<pk>\d+)/$', views.post_details, name='post_details'),
]