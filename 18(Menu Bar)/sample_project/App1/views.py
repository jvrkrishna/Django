from django.shortcuts import render

# Create your views here.
def App1_home(request):
    return render(request, 'App1_home.html')    

def App1_about(request):
    return render(request, 'about.html')

def App1_contact(request):
    return render(request, 'contact.html')

def App1_index(request):
    return render(request, 'index.html')    
