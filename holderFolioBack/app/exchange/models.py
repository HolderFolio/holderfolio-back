from django.db import models
from django.conf import settings

from holderFolioBack.models import TimeStampedModel
from app.portfolio.models import PortFolio


class Exchange(TimeStampedModel):
    STATUS_CHOICES = [
        ('Binance', 'Binance'),
        ('Kuobi', 'Kuobi'),
        ('FTX', 'FTX'),
        ('Other', 'Other')
    ]
    name = models.CharField(max_length=50, null=False, blank=False, choices=STATUS_CHOICES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    portfolio = models.ForeignKey(
        PortFolio,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = ("echanges")
   
    def __str__(self):
        return self.name
