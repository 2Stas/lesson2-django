
from django.db import models


class CustomLocation(models.Model):
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100, default="My place")
    description = models.TextField(blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
