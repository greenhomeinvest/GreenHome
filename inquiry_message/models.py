
# Create your models here.
from django.db import models


class Inquiry(models.Model):
    PROPERTY_CHOICES = [
        ('3-bed', '3-стаен'),
        ('2-bed', '2-стаен'),
        ('maisonette', 'Мезонет'),
        ('garage', 'Гараж'),
        ('shop', 'Магазин'),
    ]
   
    name = models.CharField(max_length=200, db_column='first_name')  # Allow blank and null
    phone = models.CharField(max_length=10 , db_column='phone')
    message = models.TextField(blank=True, db_column='feedback_message')
    inquiry_date = models.DateTimeField(auto_now_add=True, blank=True)
    type_property = models.CharField(max_length=20, choices=PROPERTY_CHOICES, db_column='type_property', default='Вид имот')
    
    def __str__(self):
        return f"{self.name} {self.phone}"

    class Meta:
        verbose_name_plural = "Inquiry"
        # db_table = 'feedback_message'  # Ensure this matches your actual table name
