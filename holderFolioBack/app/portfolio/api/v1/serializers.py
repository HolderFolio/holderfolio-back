from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings

from rest_framework import serializers

from app.portfolio.models import PortFolio
from app.assets.models import Asset
from app.exchange.models import Exchange
from app.exchange.api.v1.serializers import ExchangeSerializer
from app.assets.api.v1.serializers import AssetSerializer

class PortFolioSerializer(serializers.ModelSerializer):
    class Meta:
        model   = PortFolio
        fields  = ('pk','name','user',)

class PortFolioCustomeSerializer(serializers.ModelSerializer):
    exchange = serializers.SerializerMethodField()
    asset = serializers.SerializerMethodField()

    class Meta:
        model   = PortFolio
        fields  = ('pk','name','user','exchange', 'asset')

    def get_exchange(self, obj):
        exchange = Exchange.objects.filter(portfolio=obj)
        return ExchangeSerializer(exchange,many=True).data

    def get_asset(self, obj):
        asset = Asset.objects.filter(portfolio=obj)
        return AssetSerializer(asset,many=True).data
