from django.shortcuts import render,redirect

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


#Part 3 Modify the register method
# def register(request):
#     return render(request,'register.html')
from django.shortcuts import render  # For rendering templates
from django.contrib.auth.models import User  # For handling the built-in User model
from django.contrib import messages  # For displaying success or error messages
from .models import UserProfile  # Custom UserProfile model to store extra user information
import secrets  # For cryptographically secure random number generation
import string  # Provides the string constant 'digits' (0-9)

#For messages
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

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
        subject = f"Congrats {first_name} {last_name} — Your account is ready"
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER)
        to_email = [email]

        context = {'first_name': first_name, 'last_name': last_name,
                   'email': email, 'account_number': account_number}

        text_content = render_to_string('email/welcome_email.txt', context)
        html_content = render_to_string('email/welcome_email.html', context)

        try:
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, "Account created successfully! A confirmation email has been sent.")
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.exception("Failed to send welcome email")   # writes full traceback to console/log
            # log error in real app; for now show warning
            messages.warning(request, "Account created, but confirmation email could not be sent.")

        # Return the user back to the registration form with success information
        return render(request, 'register.html')

    # If it's a GET request (i.e., when the page is first accessed), show the registration form
    return render(request, 'register.html')


#Part 5 Now we are modify the Mylogin and welcome method and create logout method. 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User 

# def Mylogin(request):
#     return render(request,'login.html')

# def welcome(request):
#     return render(request,'welcome.html')
def Mylogin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('welcome')  # Redirect to the 'welcome' page after login
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')  # Stay on login page with error

    return render(request, 'login.html')

# Logout view
def Mylogout(request):
    logout(request) #Log out the current user
    messages.info(request, "You have been logged out.")
    return redirect('home')  # Redirect to home page after logout

def welcome(request):
    return render(request, 'welcome.html')

#Part 6:
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from decimal import Decimal
import csv
from .forms import DepositForm, WithdrawForm, StatementFilterForm
from .models import UserProfile, Transaction
from django.contrib import messages
from django.utils import timezone
from datetime import date

@login_required
def deposit(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description', '')
            with transaction.atomic():
                UserProfile.objects.filter(pk=profile.pk).update(balance=F('balance') + amount)
                profile.refresh_from_db()
                Transaction.objects.create(profile=profile, tx_type='deposit', amount=amount,
                                           description=description, balance_after=profile.balance)
            messages.success(request, f"Deposit successful. New balance: ₹{profile.balance:.2f}")
            return redirect('deposit')
    else:
        form = DepositForm()
    return render(request, 'deposit.html', {'form': form, 'balance': profile.balance})


@login_required
def withdraw(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description', '')
            with transaction.atomic():
                profile_locked = UserProfile.objects.select_for_update().get(pk=profile.pk)
                if profile_locked.balance < amount:
                    messages.error(request, "Insufficient balance.")
                    return render(request, 'WELCOME_PAGE/withdraw.html', {'form': form, 'balance': profile_locked.balance})
                UserProfile.objects.filter(pk=profile.pk).update(balance=F('balance') - amount)
                profile_locked.refresh_from_db()
                Transaction.objects.create(profile=profile_locked, tx_type='withdraw', amount=amount,
                                           description=description, balance_after=profile_locked.balance)
            messages.success(request, f"Withdrawal successful. New balance: ₹{profile_locked.balance:.2f}")
            return redirect('withdraw')
    else:
        form = WithdrawForm()
    return render(request, 'withdraw.html', {'form': form, 'balance': profile.balance})

@login_required
def statement(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    form = StatementFilterForm(request.GET or None)
    txs = Transaction.objects.filter(profile=profile)
    if not request.GET:
        since = timezone.now() - timezone.timedelta(days=30)
        txs = txs.filter(created_at__gte=since)
    if form.is_valid():
        choice = form.cleaned_data.get('choice')
        month = form.cleaned_data.get('month')
        year = form.cleaned_data.get('year')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        if choice == 'month' and month and year:
            start = date(year, month, 1)
            end = date(year + 1 if month==12 else year, 1 if month==12 else month+1, 1)
            txs = txs.filter(created_at__gte=start, created_at__lt=end)
        elif choice == 'year' and year:
            start, end = date(year,1,1), date(year+1,1,1)
            txs = txs.filter(created_at__gte=start, created_at__lt=end)
        elif choice == 'range' and date_from:
            if date_to:
                txs = txs.filter(created_at__date__gte=date_from, created_at__date__lte=date_to)
            else:
                txs = txs.filter(created_at__date__gte=date_from)
    txs = txs.order_by('-created_at')[:1000]
    return render(request, 'statement.html', {'form': form, 'transactions': txs,'balance': profile.balance, 'request': request})

@login_required
def export_statement_csv(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    form = StatementFilterForm(request.GET or None)
    txs = Transaction.objects.filter(profile=profile)
    if form.is_valid():
        choice = form.cleaned_data.get('choice')
        month = form.cleaned_data.get('month')
        year = form.cleaned_data.get('year')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        if choice == 'month' and month and year:
            start = date(year, month, 1)
            end = date(year + 1 if month==12 else year, 1 if month==12 else month+1, 1)
            txs = txs.filter(created_at__gte=start, created_at__lt=end)
        elif choice == 'year' and year:
            start, end = date(year,1,1), date(year+1,1,1)
            txs = txs.filter(created_at__gte=start, created_at__lt=end)
        elif choice == 'range' and date_from:
            if date_to:
                txs = txs.filter(created_at__date__gte=date_from, created_at__date__lte=date_to)
            else:
                txs = txs.filter(created_at__date__gte=date_from)
    txs = txs.order_by('-created_at')
    response = HttpResponse(content_type='text/csv')
    filename = f"statement_{profile.user.username}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(['Date','Type','Amount','Balance After','Description'])
    for t in txs:
        writer.writerow([t.created_at.strftime('%Y-%m-%d %H:%M:%S'), t.get_tx_type_display(),
                         f"{t.amount:.2f}", f"{t.balance_after:.2f}" if t.balance_after else '', t.description])
    return response