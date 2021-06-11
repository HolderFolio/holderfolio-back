from django.db import models
from django.conf import settings

from holderFolioBack.models import TimeStampedModel

class PortFolio(TimeStampedModel):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = ("PortFolios")
        

    def __str__(self):
        return self.name