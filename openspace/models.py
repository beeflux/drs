from django.contrib.gis.db import models


class Space(models.Model):
    name = models.CharField(max_length=100, default="Open Space")
    location = models.PointField()
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
