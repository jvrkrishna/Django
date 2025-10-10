from django.shortcuts import render,redirect
# Create your views here.
def home(request):
    return render(request,'home.html')
def My_login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')

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
    return render(request, 'contact_us.html')

def success(request):
    return render(request, 'success.html')