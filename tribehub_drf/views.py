from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User

from .settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)


@api_view()
def root_route(request):
    return Response({
        "message": "This is the Django Rest Framework API for TribeHub.",
    })

@api_view(['POST'])
# Fix for Django Rest Framework logout bug from Code Institute
# DRF walkthrough
def logout_route(request):
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_COOKIE_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response


class UsersList(APIView):
    """
    Returns a list of user ids and user names for testing purposes.
    Only available to users with site admin status.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.values_list('username', 'id')
        return Response({
            "users": users
        })
