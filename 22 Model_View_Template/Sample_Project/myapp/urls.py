from django.urls import path
from . import views

urlpatterns = [
    path('', views.myapp_view, name='all_posts'),
    path('rk/', views.rk_posts_view, name='rk_posts'),
]