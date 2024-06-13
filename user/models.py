from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime

class AddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.TextField(null=False,blank=False)
    city = models.CharField(max_length=20,null=False,blank=False)
    state = models.CharField(max_length=20,null=False,blank=False)
    pincode = models.CharField(max_length=7,null=False,blank=False)
    contact = models.CharField(max_length=10,null=False,blank=False)

    def __str__(self):
        return self.user.username
    
class BannedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200,null=False,blank=False)
    banned_till = models.DateField(null=True,blank=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if 'active' in kwargs:
            self.active = kwargs.pop('active')

        if not self.active:  # If active is explicitly set to False
            self.active = False  # Ensure active is False

        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.user.username} - Banned till: {self.banned_till}, Active: {self.active}"
