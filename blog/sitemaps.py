from django.contrib.sitemaps import Sitemap
from .models import Article

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    property = 0.9

    def items(self):
        return Article.published.all()

    def lasmod(self,obj):
        return obj.publish