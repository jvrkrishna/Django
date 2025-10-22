from django.contrib import admin
from .models import Contact
# Register your models here.

admin.site.register(Contact)

from .models import UserProfile
admin.site.register(UserProfile)

from .models import Transaction
admin.site.register(Transaction)