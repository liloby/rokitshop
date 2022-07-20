from django.contrib import admin
from .models import Item, Bid, Photo

# Register your models here.
admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(Photo)
