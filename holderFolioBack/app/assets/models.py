from django.db import models
from django.conf import settings

from pycoingecko import CoinGeckoAPI
import numpy as np

from holderFolioBack.models import TimeStampedModel
from app.portfolio.models import PortFolio
from app.exchange.models import Exchange


class Asset(TimeStampedModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cg = CoinGeckoAPI()
        self.paire = args[9]
        self.name = args[8]
        self.amount = args[10]
        self.price = args[11]
        self.coin = cg.get_coins_markets(ids=self.name, vs_currency=self.paire)[0]

        self.current_price_coin = np.around(self.amount * self.coin['current_price'], decimals=2)
        self.price_buy_coin = np.around(self.amount * self.price, decimals=2)
        self.win_lose_price = np.around(self.current_price_coin - self.Price_buy_coin,decimals=2)
     
    STATUS_CHOICES = [
        ('buy', 'buy'),
        ('sell', 'sell'),
        ('change', 'change'),
    ]
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    portfolio = models.ForeignKey(
        PortFolio,
        on_delete=models.CASCADE,
    )
    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
    )
    type = models.CharField(max_length=20, choices=STATUS_CHOICES, default='buy')
    name = models.CharField(max_length=100)
    paire = models.CharField(max_length=100)
    
    amount = models.IntegerField() 
    price = models.FloatField() 

    def imageSymbol(self):
        return self.coin['image']

    def currentValueCoin(self):
        value = {
            "current_price": self.coin['current_price'],
            "market_cap": self.coin['market_cap'],
            "market_cap_rank": self.coin['market_cap_rank']
        }
        return value

    def currentPrice(self):
        return  self.current_price_coin

    def invenstismentPrice(self):
        return self.price_buy_coin

    def currentPricepourcent(self):
        total = int(((100 * self.win_lose_price) / self.price_buy_coin))
        return f"{total}%"

    def winAndLost(self):
        return  np.around(self.win_lose_price, decimals=2)
        
 
    class Meta:
        verbose_name_plural = ("assets")
   
