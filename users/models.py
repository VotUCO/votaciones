from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    password = models.CharField(max_length=128, verbose_name='password', null=True)
    gender = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)

