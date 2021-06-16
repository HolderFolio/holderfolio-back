from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status, generics, permissions, authentication
from rest_framework import generics, authentication, status

from app.exchange.models import Exchange
from app.portfolio.models import PortFolio
from app.user.models import User
from app.exchange.api.v1.serializers import ExchangeSerializer

class ExchangeCreateView(generics.CreateAPIView):
    """API qui permet de créer un portfolio"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExchangeSerializer

    def post(sefl, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if request.user.is_authenticated:
            try:
                portfolio_name = request.POST.get('portfolio')
                portfolio = PortFolio.objects.get(user=request.user, pk=portfolio_name)
                if portfolio:
                    exchange = Exchange.objects.create(
                        user= request.user,
                        name= request.POST.get('name'),
                        portfolio= portfolio
                    )
                    print(exchange)
                    if exchange:
                        serializer = ExchangeSerializer(exchange, context={'request': request})
                        return Response({
                            'status_code': status.HTTP_201_CREATED,
                            'portfolio': {
                                'pk': serializer.data.get('pk'),
                                'name': serializer.data.get('name'),
                                'portfolio': serializer.data.get('portfolio'),
                                'user': serializer.data.get('user')
                            }})
            except:
                raise ObjectDoesNotExist()        

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
        if self.request.GET.get('portfolio') is not None:
            portfolio = self.request.GET.get('portfolio')
            return Exchange.objects.filter(Q(user=self.request.user) & Q(portfolio__name=portfolio))
        else: 
            raise ObjectDoesNotExist()
        