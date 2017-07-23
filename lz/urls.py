"""lz URL Configuration

"""
from django.conf.urls import url
from django.contrib import admin

from posts.feeds import LatestPostsFeed
from posts.views import index, view_post

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^feed/$', LatestPostsFeed(), name='feed'),
    url(r'^$', index, name='index'),
    url(r'^(?P<slug>[\w-]+)$', view_post, name='post')
]
