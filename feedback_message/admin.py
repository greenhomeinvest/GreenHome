from django.contrib import admin
from .models import Feedback
from django.contrib.auth.models import User 

class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    list_display = ['id', 'name', 'listing_info', 'realtor', 'user_username','feedback_date']  # Explicitly list fields
    list_display_links = ['id', 'name']

    search_fields = ['realtor__name']  # Correct the field lookup for searching
    list_per_page = 25
    
    # Automatically set all fields to be readonly
    readonly_fields = [field.name for field in Feedback._meta.fields]
    # exclude = ['listing','user_id']
    
    def listing_info(self, obj):
        estate_code = obj.listing.estate_code if obj.listing.estate_code else obj.listing.uid
        return f"{obj.listing.title} ({estate_code})"
    
    def user_username(self, obj):
        user = User.objects.get(id=obj.user_id)
        return user.username
    user_username.short_description = "Username"
       
    listing_info.short_description = "Listing Info"
admin.site.register(Feedback, FeedbackAdmin)
