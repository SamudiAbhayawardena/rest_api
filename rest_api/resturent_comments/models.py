from django.db import models

# Create your models here.
class Comments(models.Model):
    hotel_id = models.IntegerField(null=False)
    user_name = models.TextField(null=False)
    comment = models.TextField(null=False)
    write_date = models.DateTimeField(auto_now=True)