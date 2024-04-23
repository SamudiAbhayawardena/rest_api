from django.contrib import admin
from .models import User
from user_details.models import UserDetails

# Register your models here.
admin.site.register(User)
admin.site.register(UserDetails)