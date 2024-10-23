from datetime import datetime
from django.db import models
import random
import string
from realtors.models import Realtor
from multiselectfield import MultiSelectField
from django.db.models import Q
import uuid  # Import UUID for unique ID generation

class Listing(models.Model):
     # Define your choices
    OPTION_CHOICES = [
        ('Гараж', 'Гараж'),
        ('Басейн', 'Басейн'),
        ('Паркинг', 'Паркинг'),
        ('Градина', 'Градина'),
        ('В строеж', 'В строеж'),
        ('С преход', 'С преход'),
        ('Асансьор', 'Асансьор'),
        # Add external extras to OPTION_CHOICES
        ('Луксозен имот', 'Луксозен имот'),
        ('Саниран', 'Саниран'),
        ('Ток', 'Ток'),
        ('Вода', 'Вода'),
        ('Канализация', 'Канализация'),
        ('Виза', 'Виза'),
        ('В регулация', 'В регулация'),
        ('Преходен', 'Преходен'),
        ('Тежести', 'Тежести'),
        ('Таван', 'Таван'),
        ('Склад в апартамента', 'Склад в апартамента'),
        ('Технически паспорт на сградата', 'Технически паспорт на сградата'),
        ('Мазе', 'Мазе'),
        ('Идеални части от земята', 'Идеални части от земята'),
        ('Ключ', 'Ключ'),
        ('Капариран имот', 'Капариран имот'),
        ('Позволява домашен любимец', 'Позволява домашен любимец'),
        ('Намалена цена', 'Намалена цена'),
        ('За инвестиции', 'За инвестиции'),
    ]
    TYPE_CHOICES = [
        ('1-стаен', '1-стаен'),
        ('2-стаен', '2-стаен'),
        ('3-стаен', '3-стаен'),
        ('4-стаен', '4-стаен'),
        ('Многостаен', 'Многостаен'),
        ('Офис','Офис'),
        ('Студио', 'Студио'),
        ('Ателие', 'Ателие'),
        ('Мезонет', 'Мезонет'),
        ('Къща','Къща'),
        ('Етаж от къща','Етаж от къща'),
        ('Хотел','Хотел'),
        ('Парцел','Парцел'),
        ('Заведение','Заведение'),
        ('Гараж', 'Гараж'),
        ('Земеделска земя','Земеделска земя'),
    ]
    CURRENCY_CHOICES = [
        ('EUR', 'Euro'),
        ('USD', 'US Dollar'),
        ('BGN', 'Лев'),
    ]
    SIDE_CHOICES = [
        ('Западно изложение', 'Западно изложение'),
        ('Южно изложение', 'Южно изложение'),
        ('Северно изложение', 'Северно изложение'),
        ('Североизточното изложение', 'Североизточното изложение'),
        ('Северозападното изложение', 'Северозападното изложение'),
        ('Югозапад изложение', 'Югозапад изложение'),
    ]
    BUILDING_TYPE_CHOICES = [
        ('Панел', 'Панел'),
        ('Тухла', 'Тухла'),
        ('Гредоред', 'Гредоред'),
        ('ЕПК', 'ЕПК'),
        ('Сглобяема конструкция', 'Сглобяема конструкция'),
    ]
    
    uid = models.CharField(max_length=255, unique=True, null=True, blank=True)  # Add this line
    estate_code  = models.IntegerField(null=True, blank=True)
    realtor = models.ForeignKey(Realtor, on_delete=models.SET_DEFAULT, default=3, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    type_choice = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    toilet = models.IntegerField(blank=True, null=True)
    sqft = models.IntegerField(blank=True, null=True)
    floors = models.IntegerField(blank=True, null=True)
    floors_max = models.IntegerField(blank=True, null=True)
    type_building = models.CharField(max_length=30, choices=BUILDING_TYPE_CHOICES, blank=True, null=True)
    year_of_construction = models.DateField(default=datetime.now, blank=True, null=True)
    # photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now_add=True, blank=True)
    # more_options = models.ManyToManyField('MoreOptions', related_name='listings', blank=True)  # Changed related_name
    side_view = models.CharField(max_length=50, choices=SIDE_CHOICES, blank=True, null=True)
    extra_options = MultiSelectField(choices=OPTION_CHOICES, blank=True, null=True)
    
    def generate_uid(self):
        """Generate a UID in the format of 4 digits followed by 1 letter."""
        digits = ''.join(random.choices(string.digits, k=3))  # Generate 4 random digits
        letter = random.choice(string.ascii_uppercase)  # Generate 1 random uppercase letter
        return f"{digits}{letter}"  # Concatenate and return

    def save(self, *args, **kwargs):
        # Auto-generate a UID if not provided
        if not self.uid:
            self.uid = self.generate_uid()  # Call the method to generate UID
        super().save(*args, **kwargs)  # Call the original save method
    
    
    def __str__(self):
        estate_code = self.estate_code if self.estate_code else self.uid
        return f"{self.title} ({estate_code})"
    

    class Meta:
        verbose_name = "Обява"
        verbose_name_plural = "Обяви"

class Photos(models.Model):
    listing = models.ForeignKey(Listing, related_name='photos', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')

    def __str__(self):
        return self.listing.title
    
    class Meta:
        verbose_name = "Снимки"
        verbose_name_plural = "Снимки"

from django.db.models import Q

def apply_filters(queryset, request):
    # Keywords
    keywords = request.GET.get('keywords', '')
    if keywords:
        queryset = queryset.filter(
            Q(description__icontains=keywords) |
            Q(realtor__name__icontains=keywords) |
            Q(title__icontains=keywords) |
            Q(type_choice__icontains=keywords) |
            Q(extra_options__icontains=keywords) |
            Q(uid__iexact=keywords) |
            Q(estate_code__iexact=keywords)
        ).distinct()

    # City
    city = request.GET.get('city')
    if city:
        queryset = queryset.filter(city__iexact=city)

     # State
    selected_states = request.GET.getlist('state[]')
    if selected_states:
        queryset = queryset.filter(state__in=selected_states)  # Use queryset instead of queryset_list

    # Filter by building type
    selected_building_types = request.GET.getlist('building_type[]')
    if selected_building_types:
        queryset = queryset.filter(type_building__in=selected_building_types)

    # Filter by property type
    selected_property_types = request.GET.getlist('type_choice[]')
    if selected_property_types:
        queryset = queryset.filter(type_choice__in=selected_property_types)

    # Price Range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and min_price.isdigit():
        queryset = queryset.filter(price__gte=int(min_price))
    if max_price and max_price.isdigit():
        queryset = queryset.filter(price__lte=int(max_price))

    # UID or Estate Code
    uid = request.GET.get('uid')
    if uid:
        queryset = queryset.filter(estate_code__iexact=uid)
        if not queryset.exists():
            queryset = queryset.filter(uid__iexact=uid)

    return queryset
