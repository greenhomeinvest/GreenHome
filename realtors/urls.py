from django.urls import path

from realtors import views


urlpatterns = [
    path('',views.realtors , name='realtors'),
]
