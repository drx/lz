from django.contrib.syndication.views import Feed

from .models import Post


class LatestPostsFeed(Feed):
    title = "Luke Zapart"
    link = "/"
    description = ""

    def items(self):
        return Post.objects.order_by('-published_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
