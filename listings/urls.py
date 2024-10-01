from django.urls import path

from listings import views


urlpatterns = [
    path('',views.listings , name='listings'),
    path('<int:id>',views.current_listing , name='current_listing'),
    path('search',views.search , name='search'),
    path('realtor/<int:realtor_id>/listings/', views.realtor_listings, name='realtor_listings'),
]
