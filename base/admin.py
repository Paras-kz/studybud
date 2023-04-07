from django.contrib import admin

# Register your models here.
from .models import Room, Topics, Messages
admin.site.register(Room)
admin.site.register(Topics)
admin.site.register(Messages)