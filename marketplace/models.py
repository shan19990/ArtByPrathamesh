from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


# Create your models here.

class GalleryImagesModel(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to="gallery")

    def __str__(self):
        return self.title


class PaintingForSaleModel(models.Model):
    image = models.ImageField(upload_to="painting_for_sale")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    height = models.IntegerField()
    width = models.IntegerField()

    PAINTING_CHOICES = (
        ("acrylic", "Acrylic Painting"),
        ("oil", "Oil Painting"),
        ("watercolour", "Water Colour Painting"),
        ("pencilcolour", "Pencil Colour Painting"),
        ("charcoal", "Charcoal Painting"),
        ("pencilpotrait", "Pencil Potrait"),
    )

    type = models.CharField(
        max_length=20,
        choices=PAINTING_CHOICES,
        default="acrylic",
    )
    cost = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class PaintingReviewModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    painting = models.ForeignKey(PaintingForSaleModel, on_delete=models.CASCADE)
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.rating}"