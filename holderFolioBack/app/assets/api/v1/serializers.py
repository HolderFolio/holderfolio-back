from rest_framework import serializers

from pycoingecko import CoinGeckoAPI

from app.assets.models import Asset

class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Asset
        fields  = (
            'pk', 'portfolio', 'exchange', 'name','currentPricepourcent',
            'imageSymbol','invenstismentPrice','currentPrice','currentValueCoin',
            'date','amount', 'paire', 'price', 'type', 'winAndLost'
            )
