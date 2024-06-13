# Generated by Django 5.0.3 on 2024-06-12 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_banneduser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banneduser',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='banneduser',
            name='banned_till',
            field=models.DateField(blank=True, null=True),
        ),
    ]
