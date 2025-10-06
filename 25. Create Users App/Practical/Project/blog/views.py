from django.shortcuts import render,redirect
from django.contrib.auth.models import User #Here we are using existing model not creating model

# Create your views here.
def home(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        
        user=User.objects.create_user(username=username,email=email,password=password)
        user.save()
        return redirect('home') #to redirect to home page after register.
    return render(request,'register.html')

from django.contrib.auth import login,authenticate,logout
def login_user(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['pwd']
        
        user=authenticate(username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html')
    return render(request,'login.html')

def logout_user(request):
    return redirect('home')
