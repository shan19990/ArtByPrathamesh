# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from events.models import RecentEventsModel

@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    if created:
        event = f"User '{instance.email}' created an account"
        RecentEventsModel.objects.create(event=event)
