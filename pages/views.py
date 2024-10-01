from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from listings.models import Listing
from realtors.models import Realtor
from django.db.models import Count
from django.db.models import Q
import re
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from listings.choices import bedrooms_choices , price_choices,states_choices,cities_choices
# Create your views here.

from listings.models import apply_filters  # Import the utility function

def index(request):
    # Get the first 3 listings to display on the index page
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    queryset_list = Listing.objects.order_by('-list_date').filter(is_published=True)

    # Apply filters from the utility function
    queryset_list = apply_filters(queryset_list, request)

    # Extract choices
    type_choice = Listing.TYPE_CHOICES
    city_choices = Listing.objects.values_list('city', flat=True).distinct()
    state_choices = states_choices
    building_type_choices = Listing.BUILDING_TYPE_CHOICES  # Add this line

    context = {
        'listings': listings,
        'city_choices': city_choices,
        'state_choices': state_choices,
        'building_type_choices': building_type_choices,  # Include building type choices
        'type_choice': type_choice,
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
#     if request.method == 'POST':
       
#         name = request.POST['name']
#         phone = request.POST['phone']
#         subject = request.POST['subject']
#         message = request.POST['message']
 
#   # Validate phone number
#         if not re.match(r'^\d{10}$', phone):  # Check if phone consists of 10 to 15 digits
#             messages.error(request, 'Моля, въведете валиден телефонен номер (10 цифри).')
#             return render(request, 'pages/contacts.html')  # Render the form again with an error message

 
#         contact = Contact(name=name,phone=phone, message=message,subject=subject)
#         contact.save()
        

#         # Prepare the email content
#         email_subject = 'Ново запитване'
#         email_context = {
#             'name': name,
#             'phone': phone,
#             'subject':subject,
#             'message': message,
#         }
        
#         # Render the HTML template with context
#         email_body = render_to_string('contacts/email.html', email_context)
        

#         email = EmailMessage(
#         email_subject,
#         email_body,
#          'web.dev.by.vi@gmail.com',  # Your email address
#         ['web.dev.by.vi@gmail.com']
#         )
#         email.content_subtype = 'html'  # Ensure the email is sent as HTML
#         email.send()
        
#         messages.success(request, 'Вашето запитване беше изпратено успешно.')
#         return redirect('contacts')

    # Handle GET requests
    return render(request, 'pages/contacts.html')