
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings

from rest_framework import serializers

from app.user.models import User, SettingUser


class SettingsUserSerializer(serializers.ModelSerializer):
    class Meta:
        models=SettingUser
        fields= "__all__"

class UserSerializer(serializers.ModelSerializer):
    settings = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'username', 'settings'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, }, 
            # 'username': {'required': False, }, 
        }

    def get_settings(self, obj):
        user = SettingUser.objects.get(user=obj)
        serializer_settings = SettingsUserSerializer(user)
        return serializer_settings.data


class SettingsUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = SettingUser
        fields = (
            'theme', 'graphTime', 'langage', 'defaultFolio', 'devise'
        )


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {
            'html_email_template_name': 'password_reset_email.html',
            # 'subject_template_name': 'holderFolioBack.templates.password_reset_subject.txt',
        }

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)
        return value

    def save(self):
        
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'email_template_name': 'password_reset_email.html'
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)
    
    
class LoginSocialSerializer(serializers.Serializer):
    token_id = serializers.CharField(required=True)
