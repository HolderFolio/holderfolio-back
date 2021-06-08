from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from .helpers import create_user


SIGNUP_USER_URL = reverse('user:signup_user')
SIGNIN_USER_URL = reverse('user:signin_user')
UPDATE_USER_URL = reverse('user:update_user')
REST_PASSWORD_URL = reverse('user:rest_password_reset')


class PublicUserApiTests(TestCase):
    """ Test des users API (public) """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email='testuser@holderfolio.com',
            password='12Nevers34',
        )

    # CREATION DE L'UTILISATEUR
    def test_create_user_success(self):
        """ Test la création d'un user avec un bon payload """

        payload = {'email': 'testuser@holderfolio2.com','passwordConfirm':'12HolderFolio34', 'password': '12HolderFolio34'}
        res = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(res.data['status'], status.HTTP_201_CREATED)

    def test_create_user_exist(self):
        """ Test si l'utilisateur créer existe déjà  """

        payload = {'email': 'testuser@holderfolio.com','passwordConfirm':'12HolderFolio34', 'password': '12HolderFolio34'}
        res = self.client.post(SIGNUP_USER_URL, payload)
   
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_email_require(self):
        """ test que que email soit obligatoir """

        payload = {'password': '12HolderFolio34','passwordConfirm':'12HolderFolio34'}
        res = self.client.post(SIGNUP_USER_URL, payload)
      
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)       

    def test_if_token_existe_after_create_user(self):
        """ test que le token existe à la creation """

        payload = {'email': 'testuser@holderfolio3.com','passwordConfirm':'12HolderFolio34', 'password': '12HolderFolio34'}
        res = self.client.post(SIGNUP_USER_URL, payload)

        self.assertIn('token', res.data)


    # LOGIN DE L'UTILISATEUR 
    def test_signin_success(self):
        """ test que  l'user puisse bien se connecter """
        
        payload = {'email': 'testuser@holderfolio4.com', 'password': '12Nevers34'}
        create_user(**payload)
        res = self.client.post(SIGNIN_USER_URL, payload)
       
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_signin_not_exist(self):
        """ test erreur si l'user exist pas """

        payload = {'email': 'testuser@holderfolio222.com', 'password': '12Nevers34'}
        create_user(**{'email': 'testuser@holderfolio2.com', 'password': '12Nevers34'})
        res = self.client.post(SIGNIN_USER_URL, payload)
       
        self.assertEqual(res.status_code,  status.HTTP_400_BAD_REQUEST)

    def test_signin_token_in_response(self):
        """ test que  le token existe """
        
        payload = {'email': 'testuser@holderfolio5.com', 'password': '12Nevers34'}
        user = create_user(**payload)
        res = self.client.post(SIGNIN_USER_URL, payload)
        self.assertIn('token', res.data)

    # RESET PASSWORD
    def test_send_email_success(self):
        """ test que l'email soit bien envoyé """

        res = self.client.post(REST_PASSWORD_URL, {'email' : 'andres.gomesiglesias@gmail.com'})

        self.assertEqual(res.data['detail'], 'Password reset e-mail has been sent.')


class PrivateUserApiTests(TestCase):
    """ TEST API QUI ON BESOIN D AUTHENTIFICATION """

    def setUp(self):
        self.client = APIClient()
        payload = {'email': 'testuser@holderfolio.com', 'password': '12Nevers34'}
        self.user = create_user(**payload) 
        self.client.force_authenticate(user=self.user)

    # MANAGE USER ME
    def test_user_update_success(self):
        """ test update des informations de utilisateur """

        newPayload = {'username': 'newHoldername'}
        res = self.client.patch(UPDATE_USER_URL, newPayload)

        self.assertEqual(res.data['user']['username'], 'newHoldername')