# signals.py

from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import GalleryImagesModel, PaintingForSaleModel, PaintingReviewModel 
from events.models import RecentEventsModel

@receiver(post_save, sender=GalleryImagesModel)
@receiver(post_save, sender=PaintingForSaleModel)
@receiver(post_save, sender=PaintingReviewModel)
def create_event_log(sender, instance, created, **kwargs):
    if created:
        event = f"New {sender.__name__} instance created : {instance}"
        RecentEventsModel.objects.create(event=event)

@receiver(post_save, sender=GalleryImagesModel)
@receiver(post_save, sender=PaintingForSaleModel)
@receiver(post_save, sender=PaintingReviewModel)
def model_edit_event(sender, instance, created, **kwargs):
    if not created:  # Check if instance was edited
        event = f"{sender.__name__} instance edited : {instance}"
        RecentEventsModel.objects.create(event=event)


@receiver(post_delete, sender=GalleryImagesModel)
@receiver(post_delete, sender=PaintingForSaleModel)
@receiver(post_delete, sender=PaintingReviewModel)
def model_delete_event(sender, instance, **kwargs):
    event = f"{sender.__name__} instance deleted : {instance}"
    RecentEventsModel.objects.create(event=event)

