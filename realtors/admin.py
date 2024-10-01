from django.contrib import admin
from django.db import models 
# Register your models here.
from .models import Realtor

class RealtorAdmin(admin.ModelAdmin):
    model = Realtor
    list_display = ('id','get_name', 'get_phone', 'get_email', 'listing_count')  # Include listing_count in list_display
    
    def get_name(self, obj):
        return obj.name
    get_name.short_description = "Име"  # Custom display name for 'name' field

    def get_phone(self, obj):
        return obj.phone
    get_phone.short_description = "Телефон"  # Custom display name for 'phone' field

    def get_email(self, obj):
        return obj.email
    get_email.short_description = "Имейл"  # Custom display name for 'email' field

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(listing_count=models.Count('listing'))
        return queryset

    def listing_count(self, obj):
        return obj.listing_count

    listing_count.short_description = "Брой обяви"
    listing_count.admin_order_field = 'listing_count'  
    get_name.admin_order_field = 'name'
    

    
admin.site.register(Realtor, RealtorAdmin)

