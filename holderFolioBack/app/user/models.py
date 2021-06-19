from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


from app.user.manager import UserManager

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=False, null=True, blank=True, max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager() 

    def __str__(self):
        return self.email


class SettingUser(models.Model):
    THEME_CHOICES = [('light', 'light'), ('dark', 'dark')]
    GRAPHTIME_CHOICES = [('all', 'all'), ('24h', '24h')]
    LANGAGE_CHOICES = [('en', 'en'), ('fr', 'fr')]
    DIVESE_CHOICES = [('USD', 'USD'), ('EURO', 'EURO'), ('CHF', 'CHF')]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='SettingUser',
        on_delete=models.CASCADE,
        default=False
    )  
    theme = models.CharField(max_length=150, choices=THEME_CHOICES, default=THEME_CHOICES[0][0],)
    graphTime = models.CharField(max_length=150, default='all', choices=GRAPHTIME_CHOICES)
    langage = models.CharField(max_length=150, default='en', choices=LANGAGE_CHOICES)
    devise = models.CharField(max_length=150, default='USD', choices=DIVESE_CHOICES)
    defaultFolio = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        verbose_name_plural = ("SettingsUser")

    def __str__(self):
        return str(self.user.username)

  
@receiver(post_save, sender=User)
def create_user_setting(sender, instance, created, **kwargs):
    if created:
        return SettingUser.objects.create(user=instance)

  