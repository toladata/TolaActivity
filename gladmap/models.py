from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField

class Boundary(models.Model):
    geo_json = JSONField()
    country = models.CharField(max_length=100, default="None")
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.country+" "+str(self.level)

class Feature(models.Model):
    b_id = models.ForeignKey(Boundary)
    geo_json = JSONField()


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


class District(models.Model):
    boundary = JSONField()  # level 2 boundary geojson
    name = models.CharField(max_length=150, default="None") # Main-Taunus-Kreis, Nirkh
    code = models.CharField(max_length=100, default="None", unique=True) # DEU, USA, AFG etc
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.encode('ascii', 'ignore').decode('ascii') + " " + self.code
"""
Notes on GeoJson GADM Files

Level 0 - Country
Level 1 - States/Provinces
Level 2 - Districts



"""