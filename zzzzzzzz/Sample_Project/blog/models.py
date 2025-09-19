from django.db import models

# Create your models here.
from datetime import datetime
class Post(models.Model):
    title = models.CharField(max_length=150)  # Short text field
    description = models.TextField() # Large text field
    author = models.CharField(max_length=50) # Author name
    created_at = models.DateTimeField(default=datetime.now)  # Date & Time
    is_published = models.BooleanField(default=False)        # True/False

    def __str__(self):
        return self.title