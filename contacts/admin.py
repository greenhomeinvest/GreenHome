from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ['id','name', 'email', 'listing','contact_date']
    list_display_links = ['id','name']
    search_fields = ('name', 'email','listing__title', 'listing__address')
    list_per_page = 25
    
admin.site.register(Contact, ContactAdmin)
