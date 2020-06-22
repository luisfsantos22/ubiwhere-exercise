"""
This file have all the functions (converted to APIViews) for the API REST.
They are organnized by modules 'Authentication', 'Occurrences' and 'Users'.
There are two types of permission: 'AllowAny' only in 'user_registration' function
and 'IsAuthenticated' in the rest of the functions.
All the error handlers are import from a utils file.
"""
# django imports
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.measure import Distance

# rest_framework imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

# occurrence imports
from occurrences.models import Occurrences
from occurrences.utils.enums import TypeOfOccurrence
from occurrences.utils.error_handlers import (
    response_not_found,
    response_bad_request,
    response_serializer_error,
    response_insufficient_permissions,
    response_empty,
)
from occurrences.serializers import (
    OccurrencesSerializer,
    UsersSerializer,
    RegistSerializer,
    OccurrencePatchSerializer,
    OccurrenceCreateSerializer,
)

# swagger imports
from drf_yasg.utils import swagger_auto_schema


# Authentication
@swagger_auto_schema(method="post", request_body=RegistSerializer)
@api_view(["POST"])
@permission_classes((AllowAny,))
def user_registration(request):
    """
    This method allow users to regist
    """
    serializer = RegistSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        response_data = {
            "msg": "A new user has been created successfully",
            "username": user.username,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        return response_serializer_error(request, serializer)


# Occurrences
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def occurrence_list_all(request):
    """
    Method to get all occurrences and enables filters on them
    All users can call this method
    """
    occurrences = Occurrences.objects.filter().all()
    search_info = request.GET.dict()
    if search_info:
        author_search = search_info.pop("author", None)
        category_search = search_info.pop("category", None)
        location_radius = search_info.pop("radius", None)
        if author_search:
            try:
                occurrences = occurrences.filter(author_id=author_search)
            except Exception:
                occurrences = occurrences.filter(author__username=author_search)

        if category_search:
            try:
                occurrences = occurrences.filter(
                    category=TypeOfOccurrence[category_search]
                )
            except KeyError:
                return response_bad_request(request)

        if location_radius:
            actual_longitude = search_info.pop("longitude", None)
            actual_latitude = search_info.pop("latitude", None)
            if actual_longitude and actual_latitude:
                geo_point = (
                    "POINT(" + str(actual_longitude) + " " + str(actual_latitude) + ")"
                )
                occurrences = occurrences.filter(
                    geo_location__distance_lt=(geo_point, Distance(km=location_radius))
                )
            else:
                return response_bad_request(request)

    serializer = OccurrencesSerializer(occurrences, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method="post", request_body=OccurrenceCreateSerializer)
@api_view(["GET", "POST"])
@permission_classes((IsAuthenticated,))
def occurrence_own_add(request):
    """
    Method to get its own occurrences or create new ones
    All users can call this method
    """
    user = request.user
    # POST
    if request.method == "POST":
        creation_serializer = OccurrenceCreateSerializer(data=request.data)
        if creation_serializer.is_valid():
            category = TypeOfOccurrence[request.data.pop("category", None)]
            lat = request.data.pop("latitude", None)
            lon = request.data.pop("longitude", None)
            geo_point = None
            if lat and lon:
                geo_point = "POINT(" + str(lon) + " " + str(lat) + ")"
            elif lat or lon:
                return response_bad_request(request)
            serializer = OccurrencesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(geo_location=geo_point, category=category, author=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return response_serializer_error(request, serializer)
        else:
            return response_serializer_error(request, creation_serializer)

    # GET
    occurrences = Occurrences.objects.filter(author=user).all()
    serializer = OccurrencesSerializer(occurrences, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method="put", request_body=OccurrenceCreateSerializer)
@api_view(["GET", "DELETE", "PUT"])
@permission_classes((IsAuthenticated,))
def occurrences_get_update_delete(request, occurrence_id):
    """
    Method to get a specific occurrence, update its info and delete as well
    All users can call this method
    """
    try:
        occurrence = Occurrences.objects.get(id=occurrence_id)
    except Occurrences.DoesNotExist:
        return response_not_found(request)

    if request.method == "GET":
        serializer = OccurrencesSerializer(occurrence)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Only the creator of this occurrence or superusers can delete or update it
    user = request.user
    if occurrence.author != user and not user.is_superuser:
        return response_insufficient_permissions(request)

    if request.method == "PUT":
        new_data = request.data
        update_serializer = OccurrenceCreateSerializer(data=new_data)
        if new_data and update_serializer.is_valid():
            geo_location = None
            if "longitude" in request.data and "latitude" in request.data:
                actual_longitude = new_data.pop("longitude", None)
                actual_latitude = new_data.pop("latitude", None)
                geo_location = (
                    "POINT(" + str(actual_longitude) + " " + str(actual_latitude) + ")"
                )
            elif "longitude" in request.data or "latitude" in request.data:
                return response_bad_request(request)

            serializer = OccurrencesSerializer(occurrence, data=new_data)
            if serializer.is_valid():
                if geo_location:
                    serializer.save(
                        geo_location=geo_location, category=new_data["category"]
                    )
                else:
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return response_serializer_error(request, serializer)

        return (
            response_empty(request)
            if not new_data
            else response_serializer_error(request, update_serializer)
        )

    if request.method == "DELETE":
        occurrence.delete()
        return Response(
            {"msg": "Occurrence has been deleted successfully"},
            status=status.HTTP_200_OK,
        )


@swagger_auto_schema(method="patch", request_body=OccurrencePatchSerializer)
@api_view(["PATCH"])
@permission_classes((IsAuthenticated,))
def occurrences_patch(request, occurrence_id):
    """
    Method to enable the update the state of a specific occurrence
    Only superusers can call this method
    """
    try:
        occurrence = Occurrences.objects.get(id=occurrence_id)
    except Occurrences.DoesNotExist:
        return response_not_found(request)

    # Only superusers can update occurrences state
    user = request.user
    if not user.is_superuser:
        return response_insufficient_permissions(request)

    if "state" in request.data:
        serializer = OccurrencesSerializer(occurrence, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return response_serializer_error(request, serializer)

    return response_bad_request(request)


# Users
@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def user_delete(request, user_id):
    """
    Method to delete a user
    Only superusers can call this method
    """
    # Only superusers can delete users
    user = request.user
    if not user.is_superuser:
        return response_insufficient_permissions(request)

    if request.user:
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response(
                {"msg": "User has been deleted successfully"}, status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return response_not_found(request)
    else:
        return response_insufficient_permissions(request)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def users_list(request):
    """
    Method to get all non super users.
    All users can call this method
    """
    users = User.objects.filter(is_superuser=False).all()
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def users_get(request, user_id):
    """
    Method to get a specific users
    All users can call this methods
    """
    try:
        user = User.objects.get(id=user_id)
        serializer = UsersSerializer(user)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return response_not_found(request)
