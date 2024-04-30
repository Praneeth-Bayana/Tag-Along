from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15,null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    owns_car = models.BooleanField(default=False)
    organization = models.CharField(max_length=100,null=True)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']