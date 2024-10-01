from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    list_display = ['id', 'name', 'listing', 'realtor', 'feedback_date']  # Explicitly list fields
    list_display_links = ['id', 'name']
    search_fields = ['realtor__name']  # Correct the field lookup for searching
    list_per_page = 25

admin.site.register(Feedback, FeedbackAdmin)
