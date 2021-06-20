from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import (
    serializers, status, generics, permissions, authentication,
    generics, authentication, status)

from app.exchange.models import Exchange
from app.portfolio.models import PortFolio
from app.user.models import User
from app.exchange.api.v1.serializers import ExchangeSerializer

class ExchangeCreateView(generics.CreateAPIView):
    """API qui permet de créer un exchange"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExchangeSerializer

    def post(sefl, request, *args, **kwargs):
        portfolio_name = request.data['portfolio']
        exchange_name = request.data['name']
        user = request.user

        if user.is_authenticated:
            portfolio = PortFolio.objects.get(user=request.user, pk=portfolio_name)
            ifExist = Exchange.objects.filter(
                Q(name=exchange_name),
                Q(user=user),
                Q(portfolio=portfolio)).exists()
            if ifExist == False:
                for name in Exchange.STATUS_CHOICES:
                    if name[0] == exchange_name:
                        exchange = Exchange.objects.create(
                            name=exchange_name,
                            user=user,
                            portfolio=portfolio
                        )
                        serializer = ExchangeSerializer(exchange, context={'request': request})
                        return Response({
                            'status_code': status.HTTP_201_CREATED,
                            'exchange': {
                                'pk': serializer.data.get('pk'),
                                'name': serializer.data.get('name'),
                                'portfolio': serializer.data.get('portfolio'),
                                'user': serializer.data.get('user')
                                }})
                return Response({'status_code': status.HTTP_400_BAD_REQUEST, 'error': 'Wrong exchange name'})
            else:
                return Response({'status_code': status.HTTP_400_BAD_REQUEST, 'error': 'exchange allready existe'})
        return super().post(request, *args, **kwargs)            

class ExchangeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """ Permet de voir, modifier et supprimer un exchange """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExchangeSerializer
    queryset =  Exchange.objects.all()

class ExchangeListView(generics.ListAPIView):
    """ Retourn tous les portfolio lié à un user"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExchangeSerializer

    def get_queryset(self):
        portfolio = ''
        if self.request.query_params.get('portfolio'):
            portfolio = self.request.query_params.get('portfolio')
        elif self.request.data['portfolio']:
            portfolio = self.request.data['portfolio']
        return Exchange.objects.filter(Q(user=self.request.user) & Q(portfolio__name=portfolio))
  
        