from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from .helpers import create_user, create_portfolio, create_exchange


CREATE_EXCHANGE_URL = reverse('exchange:create_exchange')
LIST_EXCHANGE_URL = reverse('exchange:list_exchange')


def MANAGE_EXCHANGE_URL(id):
    return reverse('exchange:manage_exchange', kwargs={'pk': id})


class NotLoginPortFolioApiTests(TestCase):
    """ Test des portfolio API ( not login ) """

    def setUp(self):
        self.client = APIClient()

    def test_create_exchange_not_login_unauthorized(self):
        """ interdiction de créeation si l'utilisateur n'est pas loger """

        payload = {'name': 'Binance'}
        res = self.client.post(CREATE_EXCHANGE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrive_exchange_not_login_unauthorized(self):

        payload = {'email': 'testuser@holderfolio.com',
                   'password': '12Nevers34'}
        user = create_user(**payload)
        portfolio = create_portfolio(**{'user': user})
        exchange = create_exchange(**{'user': user, 'portfolio': portfolio})
        res = self.client.get(MANAGE_EXCHANGE_URL(exchange.id))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_exchange_not_login_unauthorized(self):
        res = self.client.get(LIST_EXCHANGE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePortFolioApiTests(TestCase):
    """ Test des portfolio API (privé) """

    def setUp(self):
        self.client = APIClient()
        payload = {'email': 'testuser@holderfolio.com',
                   'password': '12Nevers34'}
        self.user = create_user(**payload)
        self.portfolio = create_portfolio(**{'user': self.user})
        self.client.force_authenticate(user=self.user)

    def test_create_exchange_success(self):
        """ test la creation d'un exchange """

        payload = {'name': 'Binance',
                   'portfolio': self.portfolio.pk, 'user': self.user.pk}
        res = self.client.post(CREATE_EXCHANGE_URL, payload)

        self.assertEqual(res.data['status_code'], status.HTTP_201_CREATED)

    def test_create_exchange_wrong_name(self):
        """ test la creation d'un portfolio """

        payload = {'name': 'd', 'portfolio': self.portfolio.pk,
                   'user': self.user.pk}
        res = self.client.post(CREATE_EXCHANGE_URL, payload)

        self.assertEqual(res.status_code,  status.HTTP_400_BAD_REQUEST)

    def test_retrive_exchange_success(self):
        """ test le retour du portfolio selectionné """

        exchange = create_exchange(
            **{'user': self.user, 'portfolio': self.portfolio})
        res = self.client.get(MANAGE_EXCHANGE_URL(exchange.id))

        self.assertEqual(res.data['name'], 'Binance')

    def test_retrive_exchange_not_existe(self):
        """ test le retour du exhange selectionné n'existe pas """

        res = self.client.get(MANAGE_EXCHANGE_URL(1))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_exchange_success(self):
        """ testliest les exchange selectionné """

        portfolio = create_portfolio(
            **{'user': self.user, 'name': 'new folio'})
        exchange1 = create_exchange(
            **{'name': 'Binance', 'user': self.user, 'portfolio': self.portfolio})
        exchange2 = create_exchange(
            **{'name': 'FTX', 'user': self.user, 'portfolio': self.portfolio})
        exchange3 = create_exchange(
            **{'name': 'Kuobi', 'user': self.user, 'portfolio': portfolio})

        res = self.client.get(LIST_EXCHANGE_URL, {'portfolio': self.portfolio})

        self.assertEqual(len(res.data), 2)

    def test_update_exchange_success(self):
        """ Update le exchange """

        payload = {'name': 'FTX'}
        exchange = create_exchange(
            **{'user': self.user, 'portfolio': self.portfolio})
        res = self.client.patch(MANAGE_EXCHANGE_URL(exchange.pk), payload)

        self.assertEqual(res.data['name'], 'FTX')
