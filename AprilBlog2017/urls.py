from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from blog.views import article_list
from django.conf import settings

from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', article_list, name="index"),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



