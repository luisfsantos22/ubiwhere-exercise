"""
This file expose all the serializers that are used to convert data that can
be rendered into JSON.
They are organized by modules 'Register', 'Users' and 'Occurrences'.
"""
# django imports
from django.contrib.auth.models import User

# occurrence imports
from occurrences.models import Occurrences
from occurrences.utils.enums import TypeOfOccurrence, OccurrenceState

# rest_framework imports
from rest_framework import serializers


class RegistSerializer(serializers.ModelSerializer):
    """
    Serializer to registration method
    """

    password = serializers.CharField(write_only=True, min_length=6)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_superuser = False
        user.is_staff = False
        user.save()

        return user

    class Meta:
        model = User
        fields = ["username", "password"]


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer to users model
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class OccurrencePatchSerializer(serializers.ModelSerializer):
    """
    Serializer to occurence state verifier
    """

    state = serializers.ChoiceField(choices=OccurrenceState.choices, allow_null=False)

    class Meta:
        model = Occurrences
        fields = ["state"]


class OccurrenceCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to occurrence creation data verifier
    """

    description = serializers.CharField(required=True)
    address = serializers.CharField()
    category = serializers.ChoiceField(choices=TypeOfOccurrence.choices, required=True)
    #  temp fields
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)

    class Meta:
        model = Occurrences
        fields = ["description", "address", "category", "latitude", "longitude"]


class OccurrencesSerializer(serializers.ModelSerializer):
    """
    Serializer to occurrences model
    """

    id = serializers.ReadOnlyField()
    description = serializers.CharField()
    address = serializers.CharField()
    category = serializers.ChoiceField(choices=TypeOfOccurrence.choices, read_only=True)
    author = serializers.ReadOnlyField(source="author.username")
    state = serializers.ChoiceField(
        choices=OccurrenceState.choices,
        default=OccurrenceState.VERIFYING,
        allow_null=False
    )
    geoLocation = serializers.CharField(read_only=True, source="geo_location")
    createdAt = serializers.ReadOnlyField(source="created_at")
    modifiedAt = serializers.ReadOnlyField(source="modified_at")

    class Meta:
        model = Occurrences
        fields = [
            "id",
            "description",
            "address",
            "category",
            "author",
            "state",
            "geoLocation",
            "createdAt",
            "modifiedAt",
        ]
