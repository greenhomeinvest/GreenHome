from django.urls import path

from pages import views


urlpatterns = [
    path('',views.index, name='home'),
    path('about/',views.about, name='about'),
    path('terms/',views.terms, name='terms'),
    path('contacts/', views.contacts, name='contacts'),
]
