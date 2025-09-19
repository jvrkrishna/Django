from django.shortcuts import render
from .models import Post

# Show all posts
def myapp_view(request):
    posts = Post.objects.all()  # Fetch all posts
    return render(request, 'myapp/myapp_home.html', {'posts': posts})

# Show only posts by author "RK"
def rk_posts_view(request):
    posts = Post.objects.filter(author="RK")
    return render(request, 'myapp/myapp_home.html', {'posts': posts})