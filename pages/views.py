from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from inquiry_message.models import ImagesInquiry, Inquiry
from listings.models import Listing
from realtors.models import Realtor
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import messages
import re
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from listings.choices import bedrooms_choices , price_choices,states_choices,cities_choices
# Create your views here.

from listings.models import apply_filters  # Import the utility function

def index(request):
    # Handle the inquiry form submission
    if request.method == 'POST':
        # Print received files for debugging
        print("Files received:", request.FILES)
        images = request.FILES.getlist('images')
        print("Image list:", images)
        
        # Get form data from POST request
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        type_property = request.POST.get('type_property')
        agree = request.POST.get('agree')

        # Check if the user has agreed to the terms
        if not agree:
            messages.error(request, 'You must agree to the terms and conditions to submit the form.')
            return redirect('index')

        # Create an Inquiry instance
        inquiry_instance = Inquiry(
            name=name,
            phone=phone,
            message=message,
            type_property=type_property,  # Save the selected type_property
        )

        try:
            # Save the instance to the database
            inquiry_instance.save()
            
            # Save the uploaded images and associate them with the inquiry
            for image in images:
                ImagesInquiry.objects.create(inquiry=inquiry_instance, image=image)

            messages.success(request, 'Вашето запитване беше успешно изпратено.')
            return redirect('index')  # Redirect to 'index' after successful submission
        except Exception as e:
            messages.error(request, f'Грешка: {e}')
            print(f'Error: {e}')
            return redirect('index')  # Redirect back to the index page on error

    # Get the first 3 listings to display on the index page
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    queryset_list = Listing.objects.order_by('-list_date').filter(is_published=True)

    # Apply filters from the utility function
    queryset_list = apply_filters(queryset_list, request)
    city = request.GET.get('city')
    # Extract choices
    type_choice = Listing.TYPE_CHOICES
    city_choices = Listing.objects.values_list('city', flat=True).distinct()
    state_choices = Listing.objects.filter(city__iexact=city).values_list('state', flat=True).distinct() if city else []
    building_type_choices = Listing.BUILDING_TYPE_CHOICES  # Add this line

    context = {
        'listings': listings,
        'city_choices': city_choices,
        'state_choices': state_choices,
        'building_type_choices': building_type_choices,  # Include building type choices
        'type_choice': type_choice,
        'property_choices': Inquiry.PROPERTY_CHOICES,  
        # Add any other context variables you need
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


def contacts(request):
    return render(request, 'pages/contacts.html')