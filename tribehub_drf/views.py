from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User


@api_view()
def root_route(request):
    return Response({
        "message": "This is the Django Rest Framework API for TribeHub.",
    })


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
