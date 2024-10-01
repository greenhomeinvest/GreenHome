from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def realtors(request):
    return HttpResponse('<h1>Realtors</h1>')