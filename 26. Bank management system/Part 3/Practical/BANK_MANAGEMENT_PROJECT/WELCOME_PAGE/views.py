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
# Register view
import random
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.contrib import messages
from .models import UserProfile
from django.views.decorators.csrf import csrf_protect

def generate_12_digit_account():
    # generates a random 12-digit string (leading digit won't be zero)
    return str(random.randint(10**11, 10**12 - 1))

@csrf_protect
def register(request):
    if request.method == 'POST':
        # collect form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        account_type = request.POST.get('account_type', '').strip()
        gender = request.POST.get('gender', '').strip()
        dob = request.POST.get('dob', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        phone = request.POST.get('phone', '').strip()
        username = email

        # simple validation
        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'account_type': account_type,
            'gender': gender,
            'dob': dob,
            'address': address,
            'city': city,
            'postal_code': postal_code,
            'phone': phone,
        }

        if not all([first_name, last_name, email, account_type, gender, dob, password, password2, address, city, postal_code, phone]):
            context['error'] = "Please fill in all the required fields."
            return render(request, 'register.html', context)

        if password != password2:
            context['error'] = "Passwords do not match."
            return render(request, 'register.html', context)

        if User.objects.filter(email=email).exists():
            context['error'] = "An account with this email already exists."
            return render(request, 'register.html', context)

        # create user and profile atomically
        try:
            with transaction.atomic():
                # ensure username uniqueness; append numbers if necessary
                base_username = username or email.split('@')[0]
                final_username = base_username
                counter = 1
                while User.objects.filter(username=final_username).exists():
                    final_username = f"{base_username}{counter}"
                    counter += 1

                user = User.objects.create_user(
                    username=final_username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )

                # generate unique account number
                acct = generate_12_digit_account()
                while UserProfile.objects.filter(account_number=acct).exists():
                    acct = generate_12_digit_account()

                profile = UserProfile.objects.create(
                    user=user,
                    phone=phone,
                    gender=gender,
                    dob=dob,
                    address=address,
                    city=city,
                    postal_code=postal_code,
                    account_type=account_type,
                    account_number=acct
                )
        except IntegrityError:
            context['error'] = "Something went wrong while creating your account. Please try again."
            return render(request, 'register.html', context)

        # success — render template with success message and account number so JS can show popup
        context['success'] = True
        context['account_number'] = profile.account_number
        return render(request, 'register.html', context)

    # GET
    return render(request, 'register.html')


# Login view
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def My_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name or user.username}!")
            return redirect('welcome')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html', {'email': email})

    return render(request, 'login.html')


# Logout view
from django.contrib.auth import logout
def logout_user(request):
    logout(request) #Log out the current user
    return redirect('home')  # Redirect to home page after logout

def welcome_page(request):
    return render(request, 'welcome.html')
