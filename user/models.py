from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class AddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.TextField(null=False,blank=False)
    city = models.CharField(max_length=20,null=False,blank=False)
    state = models.CharField(max_length=20,null=False,blank=False)
    pincode = models.CharField(max_length=7,null=False,blank=False)
    contact = models.CharField(max_length=10,null=False,blank=False)

    def __str__(self):
        return self.user.username