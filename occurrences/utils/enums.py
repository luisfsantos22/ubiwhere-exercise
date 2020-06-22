"""
This file contain all the enums integrated in the models
"""
# django imports
from django.contrib.gis.db import models


class TypeOfOccurrence(models.TextChoices):
    SPECIAL_EVENT = "SPECIAL_EVENT"
    INCIDENT = "INCIDENT"
    WEATHER_CONDITION = "WEATHER_CONDITION"
    ROAD_CONDITION = "ROAD_CONDITION"


class OccurrenceState(models.TextChoices):
    VERIFYING = "VERIFYING"
    VALIDATED = "VALIDATED"
    RESOLVED = "RESOLVED"
