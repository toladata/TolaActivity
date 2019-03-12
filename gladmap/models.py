from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField

class Boundary(models.Model):
    geo_json = JSONField()
    country = models.CharField(max_length=100, default="None")
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.country+" "+str(self.level)


class Country(models.Model):
    boundary = JSONField()  # level 0 boundary geojson
    code = models.CharField(max_length=100, default="None", unique=True) # DEU, USA, AFG etc

    def __str__(self):
        return self.code


class State(models.Model):
    boundary = JSONField()  # level 1 boundary geojson
    name = models.CharField(max_length=150, default="None") # Hessen, Florida, Kunduz
    code = models.CharField(max_length=100, default="None", unique=True) # AF.KD, DE.HE
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.encode('ascii', 'ignore').decode('ascii') + " " + self.code
