from django.shortcuts import render
from django.http import HttpResponse

def home(request, param=None):
    if param is None:
        return HttpResponse("<h1>Hello Django!</h1>")
    return HttpResponse("<h1>bonjour "+ param +"!</h1>")

# Create your views here.

def contact_us(request):
    return HttpResponse("<h1>Contact Us</h1>")

def about_us(request):
    return HttpResponse("<h1>About Us</h1>")