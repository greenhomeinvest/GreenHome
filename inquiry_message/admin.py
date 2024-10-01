
from django.contrib import admin
from .models import Inquiry

class InquiryAdmin(admin.ModelAdmin):
    model = Inquiry
    list_display = ['id', 'name', 'phone','inquiry_date','type_property']  # Explicitly list fields
    list_display_links = ['id', 'name']
    
    list_per_page = 25

admin.site.register(Inquiry, InquiryAdmin)
