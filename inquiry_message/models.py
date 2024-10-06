from django.core.validators import RegexValidator
# Create your models here.
from django.db import models

#    phone_number = models.CharField(
#         max_length=20,  # Adjust based on your needs
#         validators=[
#             RegexValidator(
#                 regex=r'^\+?1?\d{9,15}$',  # Example regex for international phone numbers
#                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
#             )
#         ]
#     )
class Inquiry(models.Model):
    PROPERTY_CHOICES = [

        ('1-bed', '1-стаен'),
        ('2-bed', '2-стаен'),
        ('3-bed', '3-стаен'),
        ('4-bed', '4-стаен'),
        ('multi-bed', 'Многостаен'),
        ('office', 'Офис'),
        ('studio', 'Студио'),
        ('atelier', 'Ателие'),
        ('maisonette', 'Мезонет'),
        ('house', 'Къща'),
        ('floor-house', 'Етаж от къща'),
        ('hotel', 'Хотел'),
        ('parcel', 'Парцел'),
        ('restaurant', 'Заведение'),
        ('garage', 'Гараж'),
        ('agricultural-land', 'Земеделска земя'),
    ]
    agree_field = models.BooleanField(default=False,blank=True,null=True)
    name = models.CharField(max_length=200, db_column='first_name')  # Allow blank and null
    phone = models.CharField(max_length=10 , db_column='phone',blank=True, null=True)
    city = models.CharField(max_length=50, db_column='city', blank=True, null=True)
    message = models.TextField(blank=True, db_column='feedback_message', null=True)
    inquiry_date = models.DateTimeField(auto_now_add=True, blank=True)
    type_property = models.CharField(max_length=20, choices=PROPERTY_CHOICES, db_column='type_property', default='Вид имот',blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.phone}"

    class Meta:
        verbose_name_plural = "Inquiry"
        # db_table = 'feedback_message'  # Ensure this matches your actual table name



class ImagesInquiry(models.Model):
    inquiry = models.ForeignKey(Inquiry, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='inquiries/images/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.inquiry.name}"

    class Meta:
        verbose_name_plural = "Inquiry Images"