from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, allow_unicode=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    published_date = models.DateTimeField(blank=True)
    is_published = models.BooleanField(default=False)

    description = models.TextField(blank=True)
    text = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', args=[self.slug])
