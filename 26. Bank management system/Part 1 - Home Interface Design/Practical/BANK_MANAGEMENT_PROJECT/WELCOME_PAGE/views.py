from django.shortcuts import render

# Create your views here.
def Mylogin(request):
    return render(request,'login.html')

def welcome(request):
    return render(request,'welcome.html')

def register(request):
    return render(request,'register.html')

def contactus(request):
    return render(request, 'contactus.html')

def success(request):
    return render(request, 'success.html')