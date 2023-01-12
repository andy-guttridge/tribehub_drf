from rest_framework import status, filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response

from tribehub_drf.permissions import IsTribeAdmin, IsInTribeReadOnly
from .models import Contact
from .serializers import ContactSerializer


class ContactListCreate(generics.ListCreateAPIView):
    """
    List contacts for the user's tribe and create new
    contact if user is tribe admin
    """
    permission_classes = [IsInTribeReadOnly | IsTribeAdmin, IsAuthenticated]
    serializer_class = ContactSerializer

    def get_queryset(self):
        """
        Override get_queryset to limit results to
        only contacts for this user's tribe
        """
        user = self.request.user
        try:
            contacts_queryset = Contact.objects.filter(
                tribe=user.profile.tribe.pk
            )
        except Exception as e:
            return Response(
                str(e),
                status=status.HTTP_404_NOT_FOUND
            )
        return contacts_queryset

    def perform_create(self, serializer):
        """
        Create new contact for the tribe. Only
        allowed if user is tribe admin
        """
        # Check if user is tribe admin and create contact
        # if so. If not, raise permission denied error.
        # Have implemented manually as Django seems to ignore
        # permission classes when perform_create is
        # overriden.
        if self.request.user.profile.is_admin:
            serializer.save(
                tribe=self.request.user.profile.tribe
            )
        else:
            raise PermissionDenied


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves contact detail, allows update with PUT request
    and deletion via delete request. Users can only view contacts
    associated with their tribe. Only the tribe admin can update or
    delete contacts.
    """
    permission_classes = [IsInTribeReadOnly | IsTribeAdmin, IsAuthenticated]
    serializer_class = ContactSerializer

    def get_queryset(self):
        """
        Override get_queryset to limit results to
        only contacts for this user's tribe
        """
        user = self.request.user
        try:
            contacts_queryset = Contact.objects.filter(
                tribe=user.profile.tribe.pk
            )
        except Exception as e:
            return Response(
                str(e),
                status=status.HTTP_404_NOT_FOUND
            )
        return contacts_queryset
