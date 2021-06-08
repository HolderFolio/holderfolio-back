from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token



def create_user(**params):
    """ Helper function créer un nouvel user """

    user = get_user_model().objects.create_user(**params)
    token = Token.objects.create(user=user)

    return user