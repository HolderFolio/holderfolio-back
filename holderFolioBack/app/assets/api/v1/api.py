from django.db.models import Q

from rest_framework import generics, authentication, permissions, serializers, status
from rest_framework.response import Response

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
        response = super().post(request, *args, **kwargs)
        if request.user.is_authenticated:
            portfolio = PortFolio.objects.get(user=request.user, pk=request.POST.get('portfolio'))
            exchange = Exchange.objects.get(user=request.user, portfolio=portfolio, pk=request.POST.get('exchange'))
            asset = Asset.objects.create(
                user = request.user,
                portfolio = portfolio,
                exchange = exchange,
                date = request.POST.get('date'),
                amount = request.POST.get('amount'),
                paire = request.POST.get('paire'),
                price = request.POST.get('price'),
                type = request.POST.get('type')
            )
            if asset:
                serializer = AssetSerializer(asset, context={'request': request})
                return Response({
                    'status_code': status.HTTP_201_CREATED,
                    'data': serializer.data
                })
                

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

    def get_queryset(self):
        try:
            exchange = Asset.objects.filter(
                Q(user=self.request.user) & 
                Q(portfolio__name=self.request.GET.get('portfolio')) & 
                Q(exchange__name=self.request.GET.get('exchange')))
            return exchange
        except:
            raise ObjectDoesNotExist()
