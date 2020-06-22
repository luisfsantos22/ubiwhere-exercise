"""
This file defines the models used on the project. It contais only one class
'Occurrences' since Django automatically creates all the users structure and
this class have all the fields that we need.
"""
# django imports
from django.db import models
from django.contrib.gis.db import models as modelsGis
from django.contrib.auth.models import User

# occurrence imports
from occurrences.utils.enums import OccurrenceState, TypeOfOccurrence


# occurrences model
class Occurrences(models.Model):
    # Automatic id field
    description = models.CharField(max_length=1200)
    address = models.CharField(max_length=1200, blank=True, null=True)

    # Geo fields
    geo_location = modelsGis.PointField(blank=True, null=True)

    # Time fields
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # Enum field
    state = models.CharField(choices=OccurrenceState.choices, max_length=500)
    category = models.CharField(choices=TypeOfOccurrence.choices, max_length=500)

    # Foreign keys
    author = models.ForeignKey(User, on_delete=models.CASCADE)
