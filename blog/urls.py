from django.conf.urls import url
from . import views
from .feeds import LatestPostFeed

urlpatterns = [
    url(r'^$', views.article_list, name='article_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.article_detail, name="article_detail"),
    url(r'^tag/(?P<tag_slug>.+?)/$', views.tag_detail, name='tag_detail'),
    url(r'^tags/$', views.tag_list, name='tag_list'),
    url(r'^archives/$', views.archives, name='archives'),
    url(r'^about/$', views.aboutme, name='aboutme'),
    url(r'^about/like/$', views.like, name='like'),
    url(r'^feed/$', LatestPostFeed(), name='post_feed')
]