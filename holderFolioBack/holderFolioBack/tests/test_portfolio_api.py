import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from .helpers import create_exchange, create_user, create_portfolio, create_asset


CREATE_PORTFOLIO_URL = reverse('portfolio:create_portfolio')
LIST_PORTFOLIO_URL = reverse('portfolio:list_portfolio')

def GET_PORTFOLIO_URL(id):
        return reverse('portfolio:get_portfolio', kwargs={'pk': id})
def Gobal_RETIVE_PORTFOLIO_URL(id):
        return reverse('portfolio:global_retrive_portfolio', kwargs={'pk': id})
def MANAGE_PORTFOLIO_URL(id):
        return reverse('portfolio:update_portfolio', kwargs={'pk': id})
def RETRIVE_CUTOME_FOLIO_URL(id):
        return reverse('portfolio:retrive_custom_portfolio', kwargs={'pk': id})



class NotLoginPortFolioApiTests(TestCase):
    """ Test des portfolio API ( not login ) """
    def setUp(self):
        self.client = APIClient()

    def test_create_portfolio_not_login_unauthorized(self):
        """ interdiction de créeation si l'utilisateur n'est pas loger """

        payload = {'name': 'first folio'}
        res = self.client.post(CREATE_PORTFOLIO_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)    

    def test_get_portfolio_not_login_unauthorized(self):

        payload = {'email': 'testuser@holderfolio.com', 'password': '12Nevers34'}
        user = create_user(**payload) 
        portfolio = create_portfolio(**{'user': user})
        res = self.client.get(GET_PORTFOLIO_URL(portfolio.id))
      
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)   

    def test_list_portfolio_not_login_unauthorized(self):
        res = self.client.get(LIST_PORTFOLIO_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)  

class PrivatePortFolioApiTests(TestCase):
    """ Test des portfolio API (privé) """

    def setUp(self):
        self.client = APIClient()
        payload = {'email': 'testuser@holderfolio.com', 'password': '12Nevers34'}
        self.user = create_user(**payload) 
        self.client.force_authenticate(user=self.user)
        
    def test_create_portfolio_success(self):
        """ test la creation d'un portfolio """

        payload = {'name': 'first folio'}
        res = self.client.post(CREATE_PORTFOLIO_URL, payload)

        self.assertEqual(res.data['status_code'], status.HTTP_201_CREATED)

    def test_create_portfolio_name_empty(self):
        """ test la creation d'un portfolio nom vide"""

        payload = {'name': ''}
        res = self.client.post(CREATE_PORTFOLIO_URL, payload)

        self.assertEqual(res.data['status_code'],  status.HTTP_400_BAD_REQUEST)

    def test_create_portfolio_no_name(self):
        """ test la creation d'un portfolio sans nom """

        payload = {}
        res = self.client.post(CREATE_PORTFOLIO_URL, payload)

        self.assertEqual(res.data['status_code'],  status.HTTP_400_BAD_REQUEST)

    def test_retrive_portfolio_success(self):
        """ test le retour du portfolio selectionné """

        portfolio = create_portfolio(**{'user': self.user})
        res = self.client.get(GET_PORTFOLIO_URL(portfolio.id))
      
        self.assertEqual(res.data['name'], 'default folio')

    def test_retrive_portfolio_not_existe(self):
        """ test le retour du portfolio selectionné n'existe pas """

        res = self.client.get(GET_PORTFOLIO_URL(1))
      
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_portfolio_success(self):
        """ testliest les portfolio selectionné """

        portfolio1 = create_portfolio(**{'name': 'Folio 1', 'user':self.user})
        portfolio2 = create_portfolio(**{'name': 'Folio 2', 'user':self.user})

        res = self.client.get(LIST_PORTFOLIO_URL)

        self.assertEqual(len(res.data), 2)

    def test_update_portfolio_success(self):
        """ Update le portfolio """

        payload = {'name': 'New name'}
        portfolio = create_portfolio(**{'name': 'Folio 1', 'user':self.user})
        res = self.client.patch(MANAGE_PORTFOLIO_URL(portfolio.pk), payload)

        self.assertEqual(res.data['name'], 'New name')
    
    def test_delete_portfolio(self):
        """ test delete asset """

        portfolio = create_portfolio(**{'name': 'Folio 1', 'user':self.user})
        res = self.client.delete(MANAGE_PORTFOLIO_URL(portfolio.pk))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_retive_custom_portfolio_success(self):
        """ test que l'api retourn bien les portfolio, exchange et asset """

        portfolio = create_portfolio(**{'name': 'Folio 1', 'user':self.user})
        exchange = create_exchange(**{'user': self.user, 'portfolio': portfolio, 'name': 'Binance'})
        exchange = create_exchange(**{'user': self.user, 'portfolio': portfolio, 'name': 'FTX'})
        payload_asset = {
            'date': datetime.datetime.now(),'amount': 2,
            'paire': 'USDT','price': 10,'type': 'buy',
            'user': self.user, 'portfolio': portfolio, 'exchange': exchange
        }
        asset = create_asset(**payload_asset)
        res = self.client.get(RETRIVE_CUTOME_FOLIO_URL(portfolio.pk))
        print('data',res.data)

        self.assertIn('exchange', res.data)
        self.assertIn('asset', res.data)