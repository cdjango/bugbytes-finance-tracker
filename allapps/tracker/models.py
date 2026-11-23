from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_no = models.CharField(max_length=255)

    def __str__(self):
        return self.username
