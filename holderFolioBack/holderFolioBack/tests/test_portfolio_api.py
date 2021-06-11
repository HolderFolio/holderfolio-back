from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from .helpers import create_user, create_portfolio


CREATE_PORTFOLIO_URL = reverse('portfolio:create_portfolio')
LIST_PORTFOLIO_URL = reverse('portfolio:list_portfolio')

def GET_PORTFOLIO_URL(id):
        return reverse('portfolio:get_portfolio', kwargs={'pk': id})
def Gobal_RETIVE_PORTFOLIO_URL(id):
        return reverse('portfolio:global_retrive_portfolio', kwargs={'pk': id})
def UPDATE_PORTFOLIO_URL(id):
        return reverse('portfolio:update_portfolio', kwargs={'pk': id})



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

    def test_create_portfolio_user_forbidden(self):
        """ test la creation d'un portfolio """

        payload = {'name': 'first folio', 'user': self.user}
        res = self.client.post(CREATE_PORTFOLIO_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_portfolio_name_empty(self):
        """ test la creation d'un portfolio """

        payload = {'name': ''}
        res = self.client.post(CREATE_PORTFOLIO_URL, payload)

        self.assertEqual(res.status_code,  status.HTTP_400_BAD_REQUEST)

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
        res = self.client.patch(UPDATE_PORTFOLIO_URL(portfolio.pk), payload)

        self.assertEqual(res.data['name'], 'New name')
    
    def test_retrive_full_data_portfolio(self):
        """ retourn les datas complet pour """
        
        pass