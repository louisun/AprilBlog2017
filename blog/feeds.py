from django.contrib.syndication.views import Feed

from .models import Article

class LatestPostFeed(Feed):
    title = 'Louis\'s Blog'
    link = '/blog/'
    description_template = 'New posts of my blog'

    def items(self):
        return Article.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.html_body
