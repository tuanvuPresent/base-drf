from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from apps.user.constant import USER_TYPE, STAFF, GENDER_CHOICES, MALE


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=64, unique=True, null=True)
    user_type = models.CharField(choices=USER_TYPE, default=STAFF, max_length=8)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, default=MALE)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verify_email = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
