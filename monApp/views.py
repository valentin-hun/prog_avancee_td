from django.shortcuts import render
from django.http import HttpResponse, Http404
from monApp.models import *
from django.contrib.auth.models import User

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

def ListCategories(request):
    cats = Categorie.objects.all()
    return render(request, 'monApp/list_categories.html',{'cats': cats})

def ListStatuts(request):
    stats = Statut.objects.all()
    return render(request, 'monApp/list_statuts.html',{'stats': stats})

def ListRayon(request):
    rayons = Rayon.objects.all()
    return render(request, 'monApp/list_rayons.html',{'rayons': rayons})

def contact_us(request):
    equipe = User.objects.all()
    return render(request, 'monApp/contact_us.html',{'equipe': equipe})

def about_us(request):
    equipe = User.objects.all()
    return render(request, 'monApp/about_us.html', {'equipe': equipe})