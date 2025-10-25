from django.urls import path
from . import views

urlpatterns = [
    path('Mylogin/',views.Mylogin , name="login"),
    path('welcome/',views.welcome, name="welcome"),
    path('register/', views.register, name="register"),
    path('contactus/',views.contactus, name="contactus"),
    path('success/',views.success, name='success'),
    path('logout/',views.Mylogout,name="logout"),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('statement/', views.statement, name='statement'),
]
