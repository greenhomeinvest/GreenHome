from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from realtors.models import Realtor
from django.db.models import Q
# Create your views here.
def realtors(request):
    # realtors = Realtor.objects.all().order_by('hire_date')  # Add ordering here
    realtors = Realtor.objects.exclude(id=3).annotate(listing_count=Count('listing',filter=Q(listing__is_published=True))).order_by('hire_date')
    context = {
        'realtors': realtors
    }
    return render(request, 'realtors/realtors.html' , context)