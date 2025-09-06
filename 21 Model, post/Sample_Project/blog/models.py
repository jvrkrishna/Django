from django.db import models

# Create your models here.
from datetime import datetime
class Post(models.Model):
    title = models.CharField(max_length=150)  
    description = models.TextField() 
    author = models.CharField(max_length=50) 
    created_at = models.DateTimeField(default=datetime.now)  
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title