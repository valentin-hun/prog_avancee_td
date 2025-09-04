from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Hello Django!</h1>")

# Create your views here.

def contact_us(request):
    return HttpResponse("<h1>Contact Us</h1>")