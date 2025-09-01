from django.urls import path
from . import views
urlpatterns = [
    path('addA/', views.addAdmission),
    path('admissionR/',views.admissionReport),
]
