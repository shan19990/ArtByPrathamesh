from django.db import models

class RecentEventsModel(models.Model):
    event = models.CharField(max_length=20, null=False, blank=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.event} - {self.date}"
