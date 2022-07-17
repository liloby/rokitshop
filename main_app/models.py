from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    location = models.CharField(null=True, max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    signup_date = models.DateTimeField(('Signup Date'), auto_now_add=True)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()