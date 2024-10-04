from datetime import datetime
import hashlib
import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.temp import NamedTemporaryFile
from realtors.models import Realtor
from .models import Listing, Photos
from listings.models import apply_filters 
from listings.choices import bedrooms_choices , price_choices,states_choices,cities_choices
# from listings.models.Listing import OPTION_CHOICES
import requests
import json
# Your existing OPTION_CHOICES
OPTION_CHOICES = [
    ('Гараж', 'Гараж'),
    ('Басейн', 'Басейн'),
    ('Паркинг', 'Паркинг'),
    ('Градина', 'Градина'),
    ('В строеж', 'В строеж'),
    ('С преход', 'С преход'),
    ('Асансьор', 'Асансьор'),
    ('Луксозен имот', 'Луксозен имот'),
    ('Саниран', 'Саниран'),
    ('Ток', 'Ток'),
    ('Вода', 'Вода'),
    ('Канализация', 'Канализация'),
    ('Виза', 'Виза'),
    ('В регулация', 'В регулация'),
    ('Преходен', 'Преходен'),
    ('Тежести', 'Тежести'),
    ('Таван', 'Таван'),
    ('Склад в апартамента', 'Склад в апартамента'),
    ('Технически паспорт на сградата', 'Технически паспорт на сградата'),
    ('Мазе', 'Мазе'),
    ('Идеални части от земята', 'Идеални части от земята'),
    ('Ключ', 'Ключ'),
    ('Капариран имот', 'Капариран имот'),
    ('Позволява домашен любимец', 'Позволява домашен любимец'),
    ('Намалена цена', 'Намалена цена'),
    ('За инвестиции', 'За инвестиции'),
]


TYPE_CHOICES = [
        ('1-стаен', '1-стаен'),
        ('2-стаен', '2-стаен'),
        ('3-стаен', '3-стаен'),
        ('4-стаен', '4-стаен'),
        ('Многостаен', 'Многостаен'),
        ('Офис','Офис'),
        ('Студио', 'Студио'),
        ('Ателие', 'Ателие'),
        ('Мезонет', 'Мезонет'),
        ('Къща','Къща'),
        ('Етаж от къща','Етаж от къща'),
        ('Хотел','Хотел'),
        ('Парцел','Парцел'),
        ('Заведение','Заведение'),
        ('Гараж', 'Гараж'),
        ('Земеделска земя','Земеделска земя'),
    ]

BUILDING_TYPE_CHOICES = [
    ('Панел', 'Панел'),
    ('Тухла', 'Тухла'),
    ('Гредоред', 'Гредоред'),
    ('ЕПК', 'ЕПК'),
    ('Сглобяема конструкция', 'Сглобяема конструкция'),
]

CURRENCY_CHOICES = [
    ('EUR', 'Euro'),
    ('USD', 'US Dollar'),
    ('BGN', 'Лев'),
]

def get_building_type(build_type_name):
    for choice in BUILDING_TYPE_CHOICES:
        if build_type_name == choice[0]:
            return choice[0]  # Return the matching type name
    return ''  # Return an empty string if no match found
def get_type_choice(estate_type_name):
    for choice in TYPE_CHOICES:
        if estate_type_name == choice[0]:
            return choice[0]  # Return the matching type name
    return ''  # Return an empty string if no match found
def get_currency(currency_id):
    currency_map = {
        9: 'BGN',  # Лева
        19: 'EUR',  # Euro
        16: 'USD',  # US Dollar
    }
    return currency_map.get(currency_id, '')  # Return empty if no match
def save_image_from_url(image_url, listing):
    try:
        # Generate a unique filename using a hash of the image URL
        url_hash = hashlib.md5(image_url.encode('utf-8')).hexdigest()
        extension = os.path.splitext(image_url)[1]  # Extract extension if available
        if not extension:
            extension = '.jpg'  # Default to .jpg if no extension is provided
        
        # Construct the valid filename
        filename = f'photos/{url_hash}{extension}'
        
        # Download the image
        response = requests.get(image_url)
        response.raise_for_status() 
        
        # Save the image using default_storage
        path = default_storage.save(filename, ContentFile(response.content))
        
        # Create a new Photos object and link it to the listing
        Photos.objects.create(listing=listing, image=path)
        # print(f"Image saved successfully: {path}")
    except Exception as e:
        print(f"Error downloading or saving image: {e}")
def get_matching_extras(extras):
    extras_map = {
        14: 'в строеж',
        1: 'асансьор',
        52: 'гараж',
        93: 'с паркомясто',
        70: 'входа се заключва',
        19: 'масивна външна врата',
        40: 'сот',
        97: 'портиер / Охрана',
        3: 'луксозен имот',
        7: 'саниран',
        25: 'ток',
        24: 'вода',
        26: 'канализация',
        23: 'виза',
        29: 'в регулация',
        8: 'преходен',
        61: 'тежести',
        62: 'таван',
        63: 'склад в апартамента',
        64: 'технически паспорт на сградата',
        65: 'мазе',
        66: 'идеални части от земята',
        67: 'ключ',
        68: 'капариран имот',
        69: 'позволява домашен любимец',
        71: 'намалена цена',
        72: 'за инвестиции',
    }

    matching_extras = []
    
    # Create a set of option names for quick look-up
    option_names = {name.lower(): name for name, _ in OPTION_CHOICES}
    
    # Iterate through the extras IDs
    for extra_id in extras:
        if extra_id in extras_map:
            extra_name = extras_map[extra_id].lower()
            
            if extra_name in option_names:
                matching_extras.append(option_names[extra_name])  # Append the matched name
            
    return matching_extras




def save_listing_from_json(json_data):
    data = json.loads(json_data)
    properties = data['properties']
    brokers = {broker['id']: broker for broker in data.get('brokers', [])}

    # Get the first 10 properties, or all if there are fewer than 10
    for property in properties[:5]:  # Slice to get the first 10 properties
        uid = property.get('uid')
        estate_code = property.get('code', None)
        # Skip if this listing already exists in the database
        if Listing.objects.filter(uid=uid).exists():
            continue

        # Extract relevant data
        title = property.get('titleBG', 'No Title')
        description = property.get('DescriptionBG', 'No Description')
        price = property.get('price', 0)
        bathrooms = property.get('bathToiletCount', 1)
        sqft = property.get('space_m2', 0)
        toilet = property.get('toilet', 1)

        city = property.get('region_name', '')
        state = property.get('subregion_name') or 'Unknown'

        estate_type_name = property.get('estate_type_name', '')
        type_choice = get_type_choice(estate_type_name)
        
        build_type_name = property.get('build_type_name', '')
        type_building = get_building_type(build_type_name)

        # Handle year of construction
        year_of_construction = property.get('build_year')
        if isinstance(year_of_construction, str):
            year_of_construction = int(year_of_construction)
        if isinstance(year_of_construction, int):
            year_of_construction = datetime(year_of_construction, 1, 1)
        elif year_of_construction is None:
            year_of_construction = datetime.now()

        currency_id = property.get('currency')
        currency = get_currency(currency_id)

        person_id = property.get('person_id')
        realtor = None

        # Check if a corresponding broker exists
        if person_id and person_id in brokers:
            broker_name = brokers[person_id]['name']
            try:
                realtor = Realtor.objects.get(name=broker_name)
            except Realtor.DoesNotExist:
                realtor = Realtor.objects.get(id=3)  # Default to some fallback realtor

        # Extract the extras from the property
        extras = property.get('extras', [])
        matching_extras = get_matching_extras(extras)

        # Create the Listing object
        listing = Listing(
            uid=uid,
            estate_code=estate_code,
            title=title,
            description=description,
            price=price,
            bathrooms=bathrooms,
            sqft=sqft,
            toilet=toilet,
            city=city,
            state=state,
            type_building=type_building,
            year_of_construction=year_of_construction,
            type_choice=type_choice,
            currency=currency,
            realtor=realtor,
            extra_options=matching_extras,
        )
        
        # Save the listing to the database
        listing.save()

        # Save associated images
        for photo in property.get('photos', []):
            image_url = photo.get('url')
            save_image_from_url(image_url, listing)

                
def listings(request):
    fetch_estate_assistance_listings()

    all_listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    queryset_list = Listing.objects.order_by('-list_date').filter(is_published=True)

    # Apply filters from the utility function
    queryset_list = apply_filters(queryset_list, request)
    paginator = Paginator(all_listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    # Extract choices
    type_choice = Listing.TYPE_CHOICES
    city_choices = Listing.objects.values_list('city', flat=True).distinct()
    state_choices = states_choices
    building_type_choices = Listing.BUILDING_TYPE_CHOICES  # Add this line
    context = {
        'listings': paged_listings,
        'city_choices': city_choices,
        'state_choices': state_choices,
        'building_type_choices': building_type_choices,  # Include building type choices
        'type_choice': type_choice,
    }
    return render(request, 'listings/listings.html', context)

def fetch_estate_assistance_listings():
    # url = "http://exportdata.estateassistant.info/api/export/GetEstates/?token=a9f79df4-5570-4579-ac36-22196e1eeb6d-bdbfb59d-4757-42e4-8f77-d73b526f1edd"
    base_url = os.getenv('ESTATE_ASSISTANCE_URL')
    token = os.getenv('ESTATE_ASSISTANCE_TOKEN')

    # Construct the full URL with the token
    url = f"{base_url}?token={token}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        save_listing_from_json(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching estate assistance listings: {e}")
    

def current_listing(request,id):
    listing = get_object_or_404(Listing,pk=id)
    options = listing.extra_options or []
    # print(options)
    context = {
        'listing': listing,
        'options': options,  
        }
    return render(request, 'listings/current_listing.html',context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date').filter(is_published=True)

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                Q(description__icontains=keywords) |
                Q(realtor__name__icontains=keywords) |
                Q(title__icontains=keywords) |
                Q(type_choice__icontains=keywords) |
                Q(extra_options__icontains=keywords) |
                Q(uid__iexact=keywords)  # Search by uid if matches
                
            ).distinct()

    
    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
    
    # State
    # State
    if 'state[]' in request.GET:
        property_types = request.GET.getlist('state[]')
       
        if property_types:
            queryset_list = queryset_list.filter(state__in=property_types)
           
    # Building Type
    if 'building_type[]' in request.GET:
        building_types = request.GET.getlist('building_type[]')
        if building_types:
            queryset_list = queryset_list.filter(type_building__in=building_types)
            
    # Type Choice 
    if 'type_choice[]' in request.GET:
        property_types = request.GET.getlist('type_choice[]')
        if property_types:
            queryset_list = queryset_list.filter(type_choice__in=property_types)

    # Price Range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        queryset_list = queryset_list.filter(price__gte=min_price)
    if max_price:
        queryset_list = queryset_list.filter(price__lte=max_price)
    
    # Filter by UID (Unique ID of Listing)
    if 'uid' in request.GET:
        uid = request.GET['uid']
        if uid:
            queryset_list = queryset_list.filter(uid__iexact=uid)
    
    # Pagination
    paginator = Paginator(queryset_list, 9)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    # Extracting choices dynamically
    type_choice = Listing.TYPE_CHOICES
    city_choices = Listing.objects.values_list('city', flat=True).distinct()
    state_choices = states_choices
    price_choices = Listing.objects.values_list('price', flat=True).distinct()
    building_type_choices = Listing.BUILDING_TYPE_CHOICES
    # Debug: Print out the SQL query being executed
    # print(queryset_list.query)
    selected_states = request.GET.getlist('state[]')
    selected_building_types = request.GET.getlist('building_type[]')
    context = {
        'queryset_list': paged_listings,
        'type_choice': type_choice,
        'city_choices': city_choices,
        'state_choices': state_choices,
        'price_choices': price_choices,
        'building_type_choices': building_type_choices,
         'values': {
            'city': request.GET.get('city', ''),
            'state': selected_states,
            'min_price': request.GET.get('min_price', ''),
            'max_price': request.GET.get('max_price', ''),
            'keywords': request.GET.get('keywords', ''),
            'uid': request.GET.get('uid', ''),
            # other values
        },

    }

    return render(request, 'listings/search.html', context)


def realtor_listings(request, realtor_id):
    realtor = get_object_or_404(Realtor, id=realtor_id)
    listings = Listing.objects.filter(realtor=realtor).order_by('-list_date')
    
    context = {
        'realtor': realtor,
        'listings': listings,
    }
    return render(request, 'listings/realtor_listing.html', context)



