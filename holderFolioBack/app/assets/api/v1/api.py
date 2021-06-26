import json
import pprint

from django.db.models import Q

from rest_framework import generics, authentication, permissions, serializers, status
from rest_framework.response import Response

from pycoingecko import CoinGeckoAPI

from app.assets.api.v1.serializers import AssetSerializer
from app.assets.models import Asset
from app.portfolio.models import PortFolio
from app.exchange.models import Exchange


class AssetCreateView(generics.CreateAPIView):
    """ API qui créer un asset """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AssetSerializer

    def post(sefl, request, *args, **kwargs):
        # response = super().post(request, *args, **kwargs)
        if request.user.is_authenticated:
            portfolio_name = request.POST.get('portfolio') or request.data['portfolio']
            exchange_name = request.POST.get('exchange') or request.data['exchange']
            paire_name = request.POST.get('paire') or request.data['paire']

            portfolio = PortFolio.objects.get(user=request.user, pk=portfolio_name)
            exchange = Exchange.objects.get(user=request.user, portfolio=portfolio, pk=exchange_name)
            IExist = Asset.objects.filter(Q(user=request.user) & Q(portfolio__name=portfolio) & Q(exchange__name=exchange) & Q(paire=paire_name)).exists()
            if IExist == False:
                asset = Asset.objects.create(
                    user = request.user,
                    portfolio = portfolio,
                    exchange = exchange,
                    date = request.POST.get('date') or request.data['date'],
                    amount = request.POST.get('amount') or request.data['amount'],
                    paire = request.POST.get('paire') or request.data['paire'],
                    price = request.POST.get('price') or request.data['price'],
                    type = request.POST.get('type') or request.data['type']
                )
                serializer = AssetSerializer(asset, context={'request': request})
                return Response({
                    'status_code': status.HTTP_201_CREATED,
                    'data': serializer.data
                })
            return Response({'status_code': status.HTTP_400_BAD_REQUEST, 'error': 'Wrong asset name'})
                

class AssetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """ Permet de voir, modifier et supprimer un exchange """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AssetSerializer
    queryset =  Asset.objects.all()

class AssetListView(generics.ListAPIView):
    """ Retourn tous les portfolio lié à un user"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AssetSerializer
    queryset =  Asset.objects.all()

    def get_queryset(self):
        portfolio = ''
        exchange = ''
        if self.request.data:
            portfolio = self.request.data['portfolio']
            try:
                exchange = self.request.data['exchange']
            except:
                exchange = None
            
        else:
            portfolio = self.request.GET.get('portfolio')
            try:
                exchange = self.request.GET.get('exchange')
            except:
                exchange = None

        try:
            self.request.data['exchange']
            exchange = Asset.objects.filter(
                Q(user=self.request.user) & 
                Q(portfolio__pk=portfolio) & 
                Q(exchange__pk=exchange))
            return exchange
        except:
            exchange = Asset.objects.filter(
                Q(user=self.request.user) & 
                Q(portfolio__pk=portfolio))
            return exchange



