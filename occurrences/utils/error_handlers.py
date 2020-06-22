"""
This file contains all methods that support error handlers on this project.
The status used are: 400 (Bad Request), 401 (Unauthorized) and 404 (Not Found)
"""
# rest_framework imports
from rest_framework.response import Response
from rest_framework import status


# 400
def response_bad_request(request, exception=None):
    return Response(
        {"msg": "There is bad data in request body"}, status=status.HTTP_400_BAD_REQUEST
    )


def response_serializer_error(request, serializer, exception=None):
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 401
def response_insufficient_permissions(request, exception=None):
    return Response(
        {"msg": "Insufficient permissions to delete or update this occurrence"},
        status=status.HTTP_401_UNAUTHORIZED,
    )


# 404
def response_not_found(request, exception=None):
    return Response(
        {"msg": "Object id doenst exists"}, status=status.HTTP_404_NOT_FOUND
    )


def response_empty(request, exception=None):
    return Response(
        {"msg": "There isnt new information to update"}, status=status.HTTP_200_OK
    )
