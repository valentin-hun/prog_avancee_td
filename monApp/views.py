from django.shortcuts import render
from django.http import HttpResponse, Http404
from monApp.models import *

def home(request):
    if request.GET and request.GET["test"]:
        raise Http404
    return HttpResponse("Bonjour Monde!")

def accueil(request,param):
    return HttpResponse("<h1>Hello " + param + " ! You're connected</h1>")

# Create your views here.

def ListProduits(request):
    prdts = Produit.objects.all()
    return render(request, 'monApp/list_produits.html',{'prdts': prdts})

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