from django.shortcuts import render,redirect

# Create your views here.
def Mylogin(request):
    return render(request,'login.html')

def welcome(request):
    return render(request,'welcome.html')

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




# def register(request):
#     return render(request,'register.html')
from django.shortcuts import render  # For rendering templates
from django.contrib.auth.models import User  # For handling the built-in User model
from django.contrib import messages  # For displaying success or error messages
from .models import UserProfile  # Custom UserProfile model to store extra user information
import secrets  # For cryptographically secure random number generation
import string  # Provides the string constant 'digits' (0-9)

# Function to generate a unique 12-digit account number
def _generate_12_digit_account_number():
    digits = string.digits  # This will give us '0123456789', the digits to choose from
    while True:  # Infinite loop to keep generating account numbers until we find a unique one
        # Generate a 12-digit account number by choosing randomly from the available digits
        acct = ''.join(secrets.choice(digits) for _ in range(12))
        # Check if the account number already exists in the UserProfile table
        if not UserProfile.objects.filter(account_number=acct).exists():
            return acct  # Return the account number if it's unique

# The main register view function for handling user registration
def register(request):
    if request.method == 'POST':  # Check if the form was submitted (POST request)
        # Extract form data and strip any extra spaces
        first_name = request.POST.get('first_name', '').strip()  # First name input
        last_name = request.POST.get('last_name', '').strip()  # Last name input
        email = request.POST.get('email', '').strip()  # Email input
        account_type = request.POST.get('account_type')  # Account type (e.g., basic, premium)
        gender = request.POST.get('gender')  # Gender input
        dob = request.POST.get('dob')  # Date of birth input
        password = request.POST.get('password')  # Password input
        password2 = request.POST.get('password2')  # Password confirmation input
        address = request.POST.get('address', '').strip()  # Address input
        city = request.POST.get('city', '').strip()  # City input
        postal_code = request.POST.get('postal_code', '').strip()  # Postal code input
        phone = request.POST.get('phone', '').strip()  # Phone number input

        # Validation: Check if passwords match
        if password != password2:
            messages.error(request, "Passwords do not match.")  # Display error if passwords don't match
            # Return the user back to the registration form with the previously entered data
            return render(request, 'register.html', {
                'first_name': first_name, 'last_name': last_name, 'email': email,
                'account_type': account_type, 'gender': gender, 'dob': dob,
                'address': address, 'city': city, 'postal_code': postal_code, 'phone': phone
            })

        # Validation: Check if email already exists in the system
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")  # Display error if email is taken
            # Return the user back to the form with the previously entered data
            return render(request, 'register.html', {
                'first_name': first_name, 'last_name': last_name, 'email': email,'account_type': account_type, 'gender': gender, 'dob': dob,
                'address': address, 'city': city, 'postal_code': postal_code, 'phone': phone
            })

        # If all validations pass, create the user in the User model
        user = User.objects.create_user(username=email, email=email, password=password,first_name=first_name, last_name=last_name)
        user.save()  # Save the new user to the database

        # Generate a unique 12-digit account number for the user
        account_number = _generate_12_digit_account_number()

        # Create a UserProfile and link it to the newly created user
        UserProfile.objects.create(
            user=user,  # Link the profile to the user object
            phone=phone,  # Save the user's phone number
            gender=gender,  # Save the user's gender
            dob=dob,  # Save the user's date of birth
            address=address,  # Save the user's address
            account_number=account_number  # Save the generated unique account number
        )

        # Display success message after account creation
        messages.success(request, "Account created successfully!")

        # Return the user back to the registration form with success information
        return render(request, 'register.html')

    # If it's a GET request (i.e., when the page is first accessed), show the registration form
    return render(request, 'register.html')