from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from .helpers import create_user


SIGNUP_USER_URL = reverse('user:signup_user')
SIGNIN_USER_URL = reverse('user:signin_user')
REST_PASSWORD_URL = reverse('user:rest_password_reset')


class  PrivatePortFolioApiTests(TestCase):
    """ Test des users API (public) """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email='testuser@holderfolio.com',
            password='12Nevers34',
        )
        self.client.force_authenticate(user=self.user)
        

