
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inquiry, name='inquiry'),
    # other url patterns...
]