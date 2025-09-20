from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm

# READ - List posts
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'myapp/post_list.html', {'posts': posts})