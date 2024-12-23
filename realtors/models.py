from django.utils import timezone
from django.db import models

# Create your models here.
class Realtor(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d')
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    is_mvp = models.BooleanField(default=False)
    hire_date = models.DateTimeField(default=timezone.now, blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Брокери"