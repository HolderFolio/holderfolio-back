from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token

from app.portfolio.models import PortFolio

def create_user(**params):
    """ Helper function créer un nouvel user """

    user = get_user_model().objects.create_user(**params)
    token = Token.objects.create(user=user)

    return user

def create_portfolio(**params):
    """ creer un portfolio """

    defaults = {
        'name': 'default folio'
    }
    defaults.update(params)
    return PortFolio.objects.create(**defaults)

