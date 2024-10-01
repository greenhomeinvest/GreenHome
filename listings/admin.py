


from django.contrib import admin

# from listings.forms import MyForm

from .models import Listing, Photos
import admin_thumbnails

# Thumbnail display for photos in the admin panel
@admin_thumbnails.thumbnail('image')
class PhotosInline(admin.TabularInline):
    model = Photos
    extra = 1

# Run this command in the Django shell to add predefined options
# def add_multiple_options():
#     options = [
#         'Гараж', 'Басейн', 'Паркинг', 'Градина', 'В строеж', 'С преход', 'Асансьор'
#     ]
#     for option in options:
#         MoreOptions.objects.get_or_create(name=option)

# add_multiple_options()



class ListingAdmin(admin.ModelAdmin):
    # form = MyForm
    exclude = ('uid',) 
    list_display = ('side_view','id','uid','extra_options','title', 'type_choice', 'city', 'state', 'price', 'currency', 'is_published', 'list_date')
    list_filter = ('type_choice', 'city', 'state', 'is_published')
    search_fields = ('id','uid','title', 'city', 'state', 'description')
    list_editable = ('is_published',)
    inlines = [PhotosInline]  # Allow adding photos directly in the listing admin

admin.site.register(Listing, ListingAdmin)
# admin.site.register(MoreOptions)
