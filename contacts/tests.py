from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Contact
from profiles.models import Profile
from tribes.models import Tribe


# Create your tests here.
class ContactsListViewTests(APITestCase):
    def setUp(self):
        # Create dummy user, tribe and profile with tribe admin status
        User.objects.create_user(username='tribe_admin', password='12345')
        admin_user = User.objects.get(username='tribe_admin')
        Tribe.objects.create(name='Tribe1')
        tribe = Tribe.objects.get(name='Tribe1')
        Profile.objects.create(
            user=admin_user,
            display_name='tribe_admin',
            tribe=tribe,
            is_admin=True
        )

        # Create another dummy user without tribe admin status
        User.objects.create_user(username='tribe_member', password='12345')
        no_admin_user = User.objects.get(username='tribe_member')
        Profile.objects.create(
            user=no_admin_user,
            display_name='tribe_member',
            tribe=tribe,
            is_admin=False
        )

        # Create a contact for the tribe in the database
        Contact.objects.create(
            category='Doctor',
            company='Surgery',
            tribe=admin_user.profile.tribe
        )

    def tearDown(self):
        Profile.objects.all().delete
        Contact.objects.all().delete
        User.objects.all().delete
        Tribe.objects.all().delete

    def test_tribe_admin_can_list_contacts(self):
        User.objects.get(username='tribe_admin')
        self.client.login(username='tribe_admin', password='12345')
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tribe_member_can_list_contacts(self):
        self.client.login(username='tribe_member', password='12345')
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_list_contacts(self):
        self.client.logout()
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tribe_admin_can_create_contact(self):
        self.client.login(username='tribe_admin', password='12345')
        response = self.client.post(
          '/contacts/', {'category': 'Dentist', 'company': 'TheDentists'}
        )
        count = Contact.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tribe_member_cannot_create_contact(self):
        self.client.login(username='tribe_member', password='12345')
        response = self.client.post(
          '/contacts/', {'category': 'Dentist', 'company': 'TheDentists'}
        )
        count = Contact.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_create_contact(self):
        self.client.logout()
        response = self.client.post(
          '/contacts/', {'category': 'Dentist', 'company': 'TheDentists'}
        )
        count = Contact.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tribe_admin_can_delete_contact(self):
        self.client.login(username='tribe_admin', password='12345')
        response = self.client.delete('/contacts/1/')
        count = Contact.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_tribe_member_cannot_delete_contact(self):
        self.client.login(username='tribe_member', password='12345')
        response = self.client.delete('/contacts/1/')
        count = Contact.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_delete_contact(self):
        self.client.logout()
        response = self.client.delete('/contacts/1/')
        count = Contact.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
