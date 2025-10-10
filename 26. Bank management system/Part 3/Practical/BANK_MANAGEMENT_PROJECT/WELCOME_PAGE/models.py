from django.db import models
from datetime import datetime

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=200)
    message=models.TextField()
    is_resolved=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.email
    
    
###############################################################
# UserProfile model to store additional information about a user
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ACCOUNT_CHOICES = [
        ('savings', 'Savings'),
        ('current', 'Current'),
        ('salary', 'Salary'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)   # <-- allow NULLs
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_CHOICES)
    account_number = models.CharField(max_length=12, unique=True, blank=True)

    def __str__(self):
        return self.user.username


