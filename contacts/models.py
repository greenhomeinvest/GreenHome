from datetime import datetime
from django.db import models

from listings.models import Listing

# Create your models here.
class Contact(models.Model):
    # listing = models.CharField(max_length=200)
    # contact_id = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=datetime.now,blank=True)
    user_id = models.IntegerField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Контакти"