from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from listings.models import Listing
from realtors.models import Realtor
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from listings.choices import bedrooms_choices , price_choices,states_choices,cities_choices
# Create your views here.

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
        # Building Type
    if 'type_choice' in request.GET:
        property_type = request.GET['type_choice']
        if property_type:  # Ensure it's not empty
            queryset_list = queryset_list.filter(type__in=property_type.split(','))
     # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
    
    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)
    type_choice = Listing.TYPE_CHOICES
    city_choices = Listing.objects.values_list('city', flat=True).distinct()
    state_choices = states_choices
    context = {
        'listings': listings,
        'city_choices': city_choices,
        'state_choices': state_choices,
        'price_choices': price_choices,
        'type_choice': type_choice,
        # 'bedrooms_choices':bedrooms_choices,
      
        
    }
    return render(request, 'pages/index.html', context)

def about(request):
    realtors = Realtor.objects.annotate(listing_count=Count('listing')).order_by('-hire_date')
    
    mvp_realtors = realtors.filter(is_mvp=True)
    
    context = {
 
        'realtors': realtors,
        'mvp_realtors': mvp_realtors, 
    }
    return render(request, 'pages/about.html',context)


def terms(request):
    return render(request, 'terms/terms.html')