from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings

from rest_framework import serializers

from app.portfolio.models import PortFolio

class PortFolioSerializer(serializers.ModelSerializer):
    class Meta:
        model   = PortFolio
        fields  = ('pk','name','user',)
