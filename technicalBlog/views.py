from django.shortcuts import render
from .models import Post
from django.utils import timezone


def all_posts(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'technicalBlog/all_posts.html', {'posts': posts})

def new_post(request):
    return "new post"

def post_details(request):
    return "post details"