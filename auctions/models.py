from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from time import strftime
from PIL import Image


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField(max_length=100, blank=True, default="Unspecified")
    creation_date = models.DateTimeField(auto_now_add = True, editable=False)
    image = models.ImageField(blank=True, default='default.jpg', upload_to='listing_pics')

    def __str__(self):
        return f"{self.title}"
        
class Comment(models.Model):
    listing = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add = True, editable=False)

    class Meta:
       ordering = ('-creation_date',)

    def __str__(self):
        return '%s - %s' % (self.listing.title, self.name)