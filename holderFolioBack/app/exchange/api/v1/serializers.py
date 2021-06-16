from rest_framework import serializers

from app.exchange.models import Exchange
from app.portfolio.api.v1.serializers import PortFolioSerializer

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Exchange
        fields  = ('pk','name','user','portfolio') 