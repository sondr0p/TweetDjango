from django.contrib.postgres.fields import ArrayField
from django.db import models

class Tweet(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    hashtags = ArrayField(models.CharField(max_length=100, null=True), null=True)