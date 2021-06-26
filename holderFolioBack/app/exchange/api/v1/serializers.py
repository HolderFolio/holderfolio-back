from rest_framework import serializers

from app.exchange.models import Exchange

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Exchange
        fields  = ('pk','name','user') 