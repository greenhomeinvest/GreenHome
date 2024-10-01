from django.db import models

# Create your models here.
from django.db import models
from listings.models import Listing
from realtors.models import Realtor

class Feedback(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='feedbacks', db_column='feedback_property_id')
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE, related_name='feedbacks', db_column='feedback_realtor_id')
    name = models.CharField(max_length=200, db_column='first_name', blank=True, null=True)  # Allow blank and null
    message = models.TextField(blank=True, db_column='feedback_message')
    feedback_date = models.DateTimeField(auto_now_add=True, blank=True)
    user_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.listing.title}"

    class Meta:
        verbose_name_plural = "Feedback"
        # db_table = 'feedback_message'  # Ensure this matches your actual table name
