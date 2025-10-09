from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"at1.html")

def page1(request):
    return render(request,"at2.html")
