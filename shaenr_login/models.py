from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime

from .managers import MyUserManager


class MyUser(AbstractUser):
    """Database model for users in the system"""
    username = None
    email = models.EmailField(max_length=255, unique=False)
    email_verified = models.BooleanField(default=False)
    dob = models.DateField(default=None)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email_verified', 'dob']

    def __str__(self):
        return self.email