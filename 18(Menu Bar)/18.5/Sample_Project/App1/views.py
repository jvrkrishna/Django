from django.shortcuts import render
def App1_index(request):
    return render(request, 'index.html')

def App1_about(request):
    return render(request, 'about.html')

def App1_contact(request):
    return render(request, 'contact.html')

def App1_home(request):
    return render(request, 'App1_home.html')