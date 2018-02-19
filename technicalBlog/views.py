from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def all_posts(request):
    current_user = "Visitor"
    if request.user.is_authenticated:
        current_user = request.user
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'technicalBlog/all_posts.html', {'posts': posts, 'current_user': current_user})


@login_required(login_url='/login')
def new_post(request):
    current_user = "Visitor"
    if request.user.is_authenticated:
        current_user = request.user
        
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_details', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'technicalBlog/post_edit.html', {'form': form, 'current_user': current_user})


def post_details(request, pk):
    current_user = "Visitor"
    if request.user.is_authenticated:
        current_user = request.user

    post = get_object_or_404(Post, pk=pk)
    return render(request, 'technicalBlog/post_details.html', {'post': post, 'current_user': current_user})


@login_required(login_url='/login')
def post_edit(request, pk):
    current_user = "Visitor"
    if request.user.is_authenticated:
        current_user = request.user
        
    post = get_object_or_404(Post, pk=pk)
    
    if current_user == post.author:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_details', pk=post.pk)
        else:
            form = PostForm(instance=post)
    else:
        return redirect('post_details', pk=post.pk)
    return render(request, 'technicalBlog/post_edit.html', {'form': form, 'current_user': current_user})