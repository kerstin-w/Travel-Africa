from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Model for profile
    """

    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField("image", default="placeholder")
    description = models.TextField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=get_user_model())
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

