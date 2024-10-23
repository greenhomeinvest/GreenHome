from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import requests
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
        images = request.FILES.getlist('images')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        type_property = request.POST.get('type_property')
        agree = request.POST.get('agree')

        # Check if the user has agreed to the terms
        if not agree:
            messages.error(request, 'You must agree to the terms and conditions to submit the form.')
            return redirect('index')

        # Save the inquiry and associated images
        inquiry_instance = Inquiry(name=name, phone=phone, message=message, type_property=type_property)
        try:
            inquiry_instance.save()
            for image in images:
                ImagesInquiry.objects.create(inquiry=inquiry_instance, image=image)
            messages.success(request, 'Вашето запитване беше успешно изпратено.')
            return redirect('index')
        except Exception as e:
            messages.error(request, f'Грешка: {e}')
            return redirect('index')

    # Get the first 3 listings to display on the index page
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]

    # Get the full queryset and apply filters (if any)
    queryset_list = Listing.objects.order_by('-list_date').filter(is_published=True)
    queryset_list = apply_filters(queryset_list, request)

    # Extract choices for filters
    city_choices = Listing.objects.values_list('city', flat=True).distinct()
    state_choices = Listing.objects.filter(city__iexact=request.GET.get('city', '')).values_list('state', flat=True).distinct()
    building_type_choices = Listing.BUILDING_TYPE_CHOICES
    type_choice = Listing.TYPE_CHOICES

    context = {
        'listings': listings,
        'city_choices': city_choices,
        'state_choices': state_choices,
        'building_type_choices': building_type_choices,
        'type_choice': type_choice,
        'property_choices': Inquiry.PROPERTY_CHOICES,
        'filtered_listings': queryset_list,  # Optional, in case you want to show filtered results on the index
    }

    return render(request, 'pages/index.html', context)


def about(request):
    # api_key = 'AIzaSyCpyfYX3aKnADOjPYUvhRG9Yzf2dChb_m8'  # Replace with your actual API key
    # place_id = 'ChIJaUTS9LJVpEAR6slnfGUwjfQ'  # Replace with your actual Place ID
    realtors = Realtor.objects.annotate(listing_count=Count('listing')).order_by('-hire_date')
    
    mvp_realtors = realtors.filter(is_mvp=True)
    sections = {
        'mission': {
            'title': 'Нашата мисия',
            'description': 'Нашата мисия е да бъдем модерна компания с висок стандарт, в крак със съвременните технологии '
                           'в сектора на недвижимите имоти за постигане на максимално високи резултати. Следим световните '
                           'тенденции и прилагаме ноу-хоу в изграждането на кадрите ни. Екипът ни се състои от професионалисти, '
                           'за които клиента винаги е в центъра на всичко, което правят.',
            'image': 'img/mission2.png',
        },
        'why_green_home': {
            'title': 'Защо Green Home?',
            'description': 'Коректността, уважението и искреността са дълбоко вкоренени във фирмената ни политика. '
                           'Нашите консултанти са силно мотивирани и преминават през разнообразни обучения, за да '
                           'развиват своите знания и умения. Ние сме в постоянно търсене как да подобрим себе си '
                           'като личности и да предоставим най-доброто обслужване, за да отговорим на очакванията '
                           'на нашите клиенти.',
            'image': 'img/DSC_4781.jpg',
        }
    }
    
     # Call the Google Places API
    # url = f"https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&fields=name,rating,reviews&key={api_key}"
    # response = requests.get(url)
    reviews_code = [
    {
        'author_name': 'Petar Petrov',
        'text': 'Effective, fast, pleasant communication and feedback. Thanks for your help and honesty! I recommend.'
    },
    {
        'author_name': 'Nadezhda Mutafchieva',
        'text': 'Истински професионалисти! Много бързо работят и съдействат за абсолютно всичко!'
    },
    {
        'author_name': 'Kameliq Staneva',
        'text': 'Уникални хора, благодарение на които човек постига мечтите си! Най-вече Ралица Кръстева страхотен професионалист!'
    },
    {
        'author_name': 'Dimitar Filipovski',
        'text': 'Страхотни професионалисти! Компетентни и отзивчиви. Препоръчвам!'
    },
    {
        'author_name': 'Kaloyan Vitanov',
        'text': 'Бързо, качествено и професионално обслужване.'
    },
    {
        'author_name': 'Hristo Hristov',
        'text': 'Прекрасен екип!!'
    }
]
 # Check if the request was successful
    # if response.status_code == 200:
    #     data = response.json()
    #     print(data)  # Check the JSON response
    #     reviews = data.get('result', {}).get('reviews', [])
        
    #     # Filter reviews to only include those with a rating of 4 or higher
    #     reviews = [review for review in reviews if review.get('rating', 0) >= 4]
    # else:
    #     reviews = reviews_code 
    #     print(f"Error: {response.status_code} - {response.text}")# Handle the error case
    context = {
        'reviews':reviews_code,
        'realtors': realtors,
        'mvp_realtors': mvp_realtors, 
        'sections':sections,
    }
    return render(request, 'pages/about.html',context)


def terms(request):
    return render(request, 'terms/terms.html')


def contacts(request):
    return render(request, 'pages/contacts.html')