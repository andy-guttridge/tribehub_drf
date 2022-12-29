from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User


@api_view()
def root_route(request):
    # Returning the user ids has to be deleted before going to production!
    users = User.objects.values_list('username', 'id')
    return Response({
        "message": "This is the Django Rest Framework API for TribeHub.",
        "users": users
    })
