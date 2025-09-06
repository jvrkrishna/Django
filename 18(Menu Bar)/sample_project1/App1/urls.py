from django.urls import path
from .views import App1_index, App1_about, App1_contact, App1_home

urlpatterns = [
    path('', App1_index, name='App1_index'),
    path('about/', App1_about, name='App1_about'),
    path('contact/', App1_contact, name='App1_contact'),
    path('home/', App1_home, name='App1_home'),
]
