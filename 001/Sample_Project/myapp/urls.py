from django.urls import path
from . import views

urlpatterns = [
    path('static-example/', views.static_example, name="static_example"),
]