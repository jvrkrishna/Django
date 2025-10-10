from django.shortcuts import render,redirect
# Create your views here.
def home(request):
    return render(request,'home.html')

# #Modify Below method Accordingly
# def login(request):
#     return render(request,'login.html')

# #Modify Below method Accordingly
# def register(request):
#     return render(request,'register.html')

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




###################################################################
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
# Register view
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        gender = request.POST['gender']
        dob = request.POST['dob']
        address = request.POST['address']

        # Create user and save to database
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Now create and save the associated UserProfile
        user_profile = UserProfile.objects.create(
            user=user,
            phone=phone,
            gender=gender,
            dob=dob,
            address=address
        )
        
        return redirect('home')  # Redirect to home page after registration

    return render(request, 'register.html')


# Login view
from django.contrib import messages

def My_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Adding a success message
            messages.success(request, f"Congrats, {user.username}! You have successfully logged in.")
            return redirect('welcome')  # Redirect to the 'welcome' page after login
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')  # Stay on login page with error

    return render(request, 'login.html')

# Logout view
def logout_user(request):
    logout(request) #Log out the current user
    return redirect('home')  # Redirect to home page after logout

def welcome_page(request):
    return render(request, 'welcome.html')
