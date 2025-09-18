from django.shortcuts import render
from django.http import HttpResponse, Http404
from monApp.models import *
from django.contrib.auth.models import User
from django.views.generic import *


def accueil(request,param):
    return HttpResponse("<h1>Hello " + param + " ! You're connected</h1>")

class HomeView(TemplateView):
    template_name = "monApp/page_home.html"
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = "Hello DJANGO"
        if self.kwargs.get('param'):
            context['titreh1'] = "Hello " + self.kwargs.get('param')
        return context

class AboutView(TemplateView):
    template_name = "monApp/about_us.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
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

def ListRayons(request):
    rayons = Rayon.objects.all()
    return render(request, 'monApp/list_rayons.html',{'rayons': rayons})

def contact_us(request):
    equipe = User.objects.all()
    return render(request, 'monApp/contact_us.html',{'equipe': equipe})

def about_us(request):
    equipe = User.objects.all()
    return render(request, 'monApp/about_us.html', {'equipe': equipe})