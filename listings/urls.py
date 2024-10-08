from django.urls import path

from listings import views


urlpatterns = [
    path('all',views.listings , name='listings'),
    path('<int:id>',views.current_listing , name='current_listing'),
    path('search',views.search , name='search'),
    path('realtor/<int:realtor_id>', views.realtor_listings, name='realtor_listings'),
    path('get-states/', views.get_states, name='get_states'),
]
