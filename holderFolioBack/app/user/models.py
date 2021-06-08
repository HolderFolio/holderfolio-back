from django.db import models
from django.contrib.auth.models import AbstractUser

from . import validators
from app.user.manager import UserManager

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=False, null=True, blank=True, max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager() 

    def __str__(self):
        return self.email