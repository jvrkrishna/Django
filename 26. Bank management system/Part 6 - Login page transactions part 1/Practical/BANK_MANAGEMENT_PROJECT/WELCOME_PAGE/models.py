#Part 2
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
    
#Part 3
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    address = models.TextField()
    account_number = models.CharField(max_length=12, unique=True, blank=True)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username
    
#Part 6
class Transaction(models.Model):
    TRANSACTION_CHOICES = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    )

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transactions')
    tx_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    balance_after = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.profile.user.username} | {self.tx_type} | {self.amount}"