
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

admin.sites.AdminSite.site_header = 'Green Home'
admin.sites.AdminSite.index_title = 'Администрация'
admin.sites.AdminSite.site_title = 'Green Home'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pages.urls')),
    path('listings/',include('listings.urls')),
    path('realtors/',include('realtors.urls')),
    path('accounts/',include('accounts.urls')),
    path('contacts/',include('contacts.urls')),
    path('feedback/',include('feedback_message.urls')),
    path('inquiry/',include('inquiry_message.urls')),
]
# this is 
# + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)