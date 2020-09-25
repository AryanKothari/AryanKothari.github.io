from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from time import strftime


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField(max_length=100, blank=True)
    creation_date = models.DateTimeField(auto_now_add = True, editable=False)

    def __str__(self):
        return f"{self.title}"
