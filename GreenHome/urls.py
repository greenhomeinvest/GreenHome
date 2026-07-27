
from django.contrib import admin
from django.urls import path,include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

admin.sites.AdminSite.site_header = 'Green Home'
admin.sites.AdminSite.index_title = 'Администрация'
admin.sites.AdminSite.site_title = 'Green Home'

urlpatterns = [
    path('adminGH2022/', admin.site.urls),
    path('',include('pages.urls')),
    path('imoti-obiavi/',include('listings.urls')),
    path('realtors/',include('realtors.urls')),
    path('accounts/',include('accounts.urls')),
    path('contact/',include('contacts.urls')),
    path('feedback/',include('feedback_message.urls')),
    path('/',include('inquiry_message.urls')), 
    # inquiry url
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
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)