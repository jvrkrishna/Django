from django.shortcuts import render,redirect

# Create your views here.
def Mylogin(request):
    return render(request,'login.html')

def welcome(request):
    return render(request,'welcome.html')

def register(request):
    return render(request,'register.html')

# def contactus(request):
#     return render(request, 'contactus.html')

#Part 2---Modify Above Contactus method
from .models import Contact
def contactus(request):
    if request.method == 'POST':
        # use .get with default '' to avoid KeyError
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()   # match your template's name attr ('message')

        # Save to DB
        contact = Contact(name=name, email=email, message=message)
        contact.save()

        # Redirect to a success page (Post/Redirect/Get)
        return redirect('success')   # name of the success url pattern

    # GET request, show blank form
    return render(request, 'contactus.html')

def success(request):
    return render(request, 'success.html')
