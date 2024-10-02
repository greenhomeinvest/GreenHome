
from django.contrib import admin
from .models import ImagesInquiry, Inquiry


import admin_thumbnails

# Thumbnail display for photos in the admin panel
@admin_thumbnails.thumbnail('image')
class ImagesInline(admin.TabularInline):
    model = ImagesInquiry
    extra = 1


class InquiryAdmin(admin.ModelAdmin):
    model = Inquiry
    list_display = ['id', 'name', 'phone','inquiry_date','type_property']  # Explicitly list fields
    list_display_links = ['id', 'name']
    inlines = [ImagesInline] 
    list_per_page = 25

admin.site.register(Inquiry, InquiryAdmin)
