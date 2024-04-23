from django.db import models
from accounts.models import User


class UserDetails(models.Model):
    user_res = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    profile = models.CharField(max_length=200,null=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=20, null=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    diabetics_score = models.FloatField(null=True)
    veg_status = models.CharField(max_length=30, null=True)

    
     
