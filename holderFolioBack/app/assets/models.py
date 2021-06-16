from django.db import models
from django.conf import settings

from holderFolioBack.models import TimeStampedModel
from app.portfolio.models import PortFolio
from app.exchange.models import Exchange


class asset(TimeStampedModel):
    STATUS_CHOICES = [
        ('buy', 'buy'),
        ('sell', 'sell'),
        ('change', 'change'),
    ]
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

    date = models.DateTimeField(null=True, blank=True)
    amount = models.IntegerField()
    paire = models.CharField(max_length=100)
    price = models.IntegerField()
    type = models.CharField(max_length=20, choices=STATUS_CHOICES, default='buy')

 
    class Meta:
        verbose_name_plural = ("assets")
   
