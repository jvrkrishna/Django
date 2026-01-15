from django.urls import path
from .views import contactus,success

urlpatterns=[
    path('',contactus,name='contactus'),
    path('success/',success,name='success')
]