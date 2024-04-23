from django.db import models
from accounts.models import User


class HealthHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diabetics_score = models.FloatField(null=False)
    weight = models.FloatField(null=True)
    calories = models.FloatField(null=True)
    carbs = models.FloatField(null=True)
    fat = models.FloatField(null=True)
    proteins = models.FloatField(null=True)
