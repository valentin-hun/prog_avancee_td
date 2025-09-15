from django.shortcuts import render
from django.http import HttpResponse
from monApp.models import *

def home(request, param=None):
    if param is None:
        return HttpResponse("<h1>Hello Django!</h1>")
    return HttpResponse("<h1>bonjour "+ param +"!</h1>")

# Create your views here.

def liste_produits(request):
    prdts = Produit.objects.all()
    res = ""
    for prod in prdts:
        res += "<li>" + prod.intituleProd + "</li>" 
    return HttpResponse("<ul>"+ res +"</ul>")

def categories(request):
    cats = Categorie.objects.all()
    res = ""
    for cat in cats:
        res += "<li>" + cat.nomCat + "</li>" 
    return HttpResponse("<ul>"+ res +"</ul>")

def statuts(request):
    stats = Statut.objects.all()
    res = ""
    for stat in stats:
        res += "<li>" + stat.libelle + "</li>" 
    return HttpResponse("<ul>"+ res +"</ul>")

def contact_us(request):
    return HttpResponse("<h1>Contact Us</h1>")

def about_us(request):
    return HttpResponse("<h1>About Us</h1>")