from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    date = models.DateField('Upload Date')
    description = models.TextField(max_length=250)
    posted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", kwargs={"item_id": self.pk})
    