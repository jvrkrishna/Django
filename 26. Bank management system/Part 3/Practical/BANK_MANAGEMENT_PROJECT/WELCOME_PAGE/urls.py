from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.My_login, name="login"),
    path('register/', views.register, name="register"),
    path('contactus/',views.contactus,name='contactus'),
    path('success/',views.success,name='success'),
    path('welcome/',views.welcome_page, name='welcome'),
    path('logout/', views.logout_user, name='logout'),
]

