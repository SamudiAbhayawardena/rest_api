from django.db import models
from accounts.models import User

# Create your models here.
class Notifications(models.Model):
    user_res = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.TextField(null=False)
    description = models.TextField(null=False)
    status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
