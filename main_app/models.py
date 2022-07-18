from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from datetime import datetime, date
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    date = models.DateField(('Upload Date'), auto_now_add=True)
    description = models.TextField(max_length=250)
    posted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", kwargs={"item_id": self.pk})
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    location = models.CharField(null=True, max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
        
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    


