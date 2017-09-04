from django.shortcuts import get_object_or_404, render

from .models import Post


def index(request):
    posts = Post.objects.filter(is_published=True).order_by('-published_date')
    return render(request, 'index.html', {'posts': posts})


def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'posts/post.html', {'post': post})
