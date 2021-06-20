import datetime
from app.exchange.models import Exchange
from app.portfolio.models import PortFolio

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from .helpers import create_user, create_portfolio, create_exchange, create_asset


CREATE_ASSET_URL = reverse('asset:create_asset')
LIST_ASSET_URL = reverse('asset:list_asset')

def MANAGE_ASSET_URL(id):
    return reverse('asset:manage_asset', kwargs={'pk': id})


class NotLoginPortFolioApiTests(TestCase):
    """ Test des portfolio API ( not login ) """

    def setUp(self):
        self.client = APIClient()

    def test_create_asset_not_login_unauthorized(self):
        """ interdiction de créeation si l'utilisateur n'est pas loger """

        payload = {'user': ''}
        res = self.client.post(CREATE_ASSET_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrive_exchange_not_login_unauthorized(self):

        payload = {'email': 'testuser@holderfolio.com',
                   'password': '12Nevers34'}
        user = create_user(**payload)
        portfolio = create_portfolio(**{'user': user})
        exchange = create_exchange(**{'user': user, 'portfolio': portfolio})
        res = self.client.get(MANAGE_ASSET_URL(exchange.id))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_asset_not_login_unauthorized(self):
        res = self.client.get(LIST_ASSET_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePortFolioApiTests(TestCase):
    """ Test des portfolio API (privé) """

    def setUp(self):
        self.client = APIClient()
        payload_user = {'email': 'testuser@holderfolio.com','password': '12Nevers34'}
        self.user = create_user(**payload_user)
        self.portfolio = create_portfolio(**{'user': self.user})
        self.exchange = create_exchange(**{'user': self.user, 'portfolio': self.portfolio, 'name': 'Binance'})
        self.payload_asset = {
            'date': datetime.datetime.now(),'amount': 2,
            'paire': 'USDT','price': 10,'type': 'buy',
            'user': self.user.pk, 'portfolio': self.portfolio.pk, 'exchange': self.exchange.pk
        }
    
        self.client.force_authenticate(user=self.user)

    def test_create_asset_success(self):
        """ test la creation d'un exchange """
    
        res = self.client.post(CREATE_ASSET_URL, self.payload_asset)

        self.assertEqual(res.data['status_code'], status.HTTP_201_CREATED)

    def test_retrive_asset_success(self):
        """ test le retour du asset selectionné """
        payload_asset = {
            'date': datetime.datetime.now(),'amount': 2,
            'paire': 'USDT','price': 10,'type': 'buy',
            'user': self.user, 'portfolio': self.portfolio, 'exchange': self.exchange
        }
        exchange = create_asset(**payload_asset)
        res = self.client.get(MANAGE_ASSET_URL(exchange.id))

        self.assertEqual(res.data['paire'], 'USDT')

    def test_retrive_asset_not_existe(self):
        """ test le retour duasset selectionné n'existe pas """

        res = self.client.get(MANAGE_ASSET_URL(1))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_asset_success(self):
        """ testliest les asset selectionné """

        asset1 = create_asset(
            **{'exchange': self.exchange, 'user': self.user, 'portfolio': self.portfolio})
        asset2 = create_asset(
            **{'exchange': self.exchange, 'user': self.user, 'portfolio': self.portfolio})
            
        payload ={'portfolio': self.portfolio.pk, 'exchange': self.exchange.pk}
        res = self.client.get(LIST_ASSET_URL, payload)

        self.assertEqual(len(res.data), 2)

    def test_update_asset_success(self):
        """ Update l'asset """

        payload = {'amount': '1000'}
        asset = create_asset(
            **{'exchange': self.exchange, 'user': self.user, 'portfolio': self.portfolio})
        res = self.client.patch(MANAGE_ASSET_URL(asset.pk), payload)

        self.assertEqual(res.data['amount'], 1000)
    
    def test_delete_asset(self):
        """ test delete asset """

        asset = create_asset(
            **{'exchange': self.exchange, 'user': self.user, 'portfolio': self.portfolio})
        res = self.client.delete(MANAGE_ASSET_URL(asset.pk))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)