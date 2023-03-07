from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser, UserManager



class Profile(models.Model):
    """
    Model for profile
    """
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image', default='placeholder')
    description = models.TextField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
        
