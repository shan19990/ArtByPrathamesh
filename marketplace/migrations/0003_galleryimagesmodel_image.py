# Generated by Django 5.0.3 on 2024-05-15 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_remove_galleryimagesmodel_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimagesmodel',
            name='image',
            field=models.ImageField(default='', upload_to='images'),
            preserve_default=False,
        ),
    ]
